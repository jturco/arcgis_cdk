from aws_cdk import(
    aws_s3 as s3,
    aws_ec2 as ec2,
    aws_iam as iam,
    aws_route53 as r53,
    aws_elasticloadbalancingv2 as elbv2,
    aws_elasticloadbalancingv2_targets as elbv2_targets,
    core
)

import os, json, logging, datetime, time

def get_logger(log_name, log_dir, run_name):

    the_logger = logging.getLogger(run_name)
    the_logger.setLevel(logging.DEBUG)

    # Ensure Directories Exist
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)

    # Set Console Handler
    ch = logging.StreamHandler()
    ch.setLevel(logging.INFO)

    # Set File Handler
    fh = logging.FileHandler(os.path.join(log_dir, log_name), 'a')
    fh.setLevel(logging.DEBUG)

    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

    ch.setFormatter(formatter)
    fh.setFormatter(formatter)

    the_logger.addHandler(ch)
    the_logger.addHandler(fh)

    the_logger.info('Logger Initialized')

    return the_logger

def clean_logs(log_dir):

    if not os.path.exists(log_dir):
        return

    for f in os.listdir(log_dir):
        os.remove(os.path.join(log_dir, f))

def get_config(in_file):

    with open(in_file) as config:
        param_dict = json.load(config)

    return param_dict

start_time = time.time()
this_dir = os.path.split(os.path.realpath(__file__))[0]
t_format = datetime.datetime.fromtimestamp(start_time).strftime('%d_%m_%H_%M_%S')
log_name = f'ARCGIS_CDK_{t_format}.log'
log_dir = os.path.join(this_dir, 'logs')
logger = get_logger(log_name, log_dir, 'LOGGER')
config_file = os.path.join(this_dir, 'arcgis_cdk_config.json')

# Get Configuration Parameters
params = get_config(config_file)
config = params["configuration"]
instances = params["instances"]
rdp_ingress = params["security_group_ingress"]["ip_address"]

class ArcgisCdkStack(core.Stack):

    def __init__(self, scope: core.Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)
        logger.info('Initializing ArcGIS Cdk Stack')
        logger.info(f'Customer - {config["customer"]}')
        # The code that defines your stack goes here
        logger.info('Creating deployment bucket inside cdk stack')
        deployment_bucket = s3.Bucket(self,
            config["customer"] + "_" +"arcgis_cdk_bucket"
        )

        logger.info('Creating VPC inside cdk stack')
        vpc = ec2.Vpc(self, config["customer"] + "_" +"arcgis_cdk_vpc")
        logger.info('Private Subnet 1 - ')
        logger.info(vpc.private_subnets[0])
        logger.info('Public Subnet 1 - ')
        logger.info(vpc.public_subnets[0])

        r53_phz = r53.PrivateHostedZone(self, id=config["customer"] + "_" + "phz", vpc=vpc, zone_name=config["customer"]+".com")

        logger.info('Creating Security Groups')
        sg_public = ec2.SecurityGroup(self, config["customer"] + "_" + "sg_public", vpc=vpc, security_group_name=config["customer"] + "_" + "arcgis_sg_public")
        sg_private = ec2.SecurityGroup(self, config["customer"] + "_" + "sg_private", vpc=vpc, security_group_name=config["customer"] + "_" + "arcgis_sg_private")
        # sg_public_connection = ec2.Connections("443", sg_public)
        sg_private.add_ingress_rule(peer=sg_public , connection=ec2.Port.tcp(443))
        sg_private.add_ingress_rule(peer=sg_public , connection=ec2.Port.tcp(3389))
        sg_private.add_ingress_rule(peer=sg_public , connection=ec2.Port.tcp(5985))
        sg_private.add_ingress_rule(peer=sg_public , connection=ec2.Port.tcp(5986))
        sg_private.add_ingress_rule(peer=sg_private , connection=ec2.Port.all_traffic())
        sg_public.add_ingress_rule(peer=ec2.Peer.any_ipv4(), connection=ec2.Port.tcp(443))
        # sg_public.add_ingress_rule(peer=ec2.Peer.any_ipv4(), connection=ec2.Port.all_traffic())
        sg_public.add_ingress_rule(peer=ec2.Peer.ipv4(rdp_ingress), connection=ec2.Port.tcp(3389))
        
        logger.info('Creating IAM Role for insances...')
        role = iam.Role(self, config["customer"] + "-" + "arcgis-ec2-iam-role", assumed_by=iam.ServicePrincipal("ec2.amazonaws.com"))
        role.add_managed_policy(iam.ManagedPolicy.from_aws_managed_policy_name("service-role/AmazonEC2RoleforSSM"))
        role.add_managed_policy(iam.ManagedPolicy.from_aws_managed_policy_name("AmazonS3FullAccess"))
        # Add Access to Above S3 Bucket....
        # listener = alb.add_listener("Listener", port=80)

        if params['configuration']['high_availability'] == "true":
            #duplicate each instances
            logger.info('Found an HA Implementation duplicating resources and adding fileshare')
            # duplicate each instanc
            fileserver = {}
            logger.info(config)
            # Set a list to handle the new instances
            ha_instances = []
            for instance in instances:
                ha_instance = {}
                # Change tag of original
                instances[instance]['tag'] = config["customer"] + "_" + instances[instance]["tag"] + "_01"
                ha_instance[instance + "_02"] = {}
                instance_tag = instances[instance]["tag"][:-3] + "_02"
                ha_instance[instance + "_02"]["tag"] = instance_tag
                ha_instance[instance + "_02"]["size"] = instances[instance]["size"]
                ha_instance[instance + "_02"]["subnet"] = instances[instance]["subnet"]
                ha_instances.append(ha_instance)
            logger.info(ha_instances)
            fileserver["tag"] = config["customer"] + "_fileserver_01"
            fileserver["size"] = config["file_server_size"]
            fileserver["subnet"] = "private"
            instances[instance] = fileserver
            for ha_instance in ha_instances:
                logger.info(ha_instance)
                for ha_dict in ha_instance:
                    instances[ha_dict] = ha_instance[ha_dict]

        # loop thru a config file that gives details for each isntance
        logger.info('Creating EC2 Instances from JSON file')
        portal_instances = []
        server_instances = []
        for instance in instances:
            logger.info(f'Setting up EC2 Instance Object for - {instance}')
            logger.debug(instances[instance])
            instance_type = instances[instance]['size']
            instance_tag =  instances[instance]['tag']
            subnet = instances[instance]['subnet']
            # Will need to handle HA here
            if subnet == "private":
                logger.info(f'Deploying {instance} into private subnet')
                instance_subnet = ec2.SubnetSelection(subnets=vpc.private_subnets)
                security_group = sg_private
            if subnet == "public": 
                logger.info(f'Deploying {instance} into public subnet')
                instance_subnet = ec2.SubnetSelection(subnets=vpc.public_subnets)
                security_group = sg_public
            ec2_instance_type = ec2.InstanceType(instance_type)
            ec2_machine_image = ec2.MachineImage.latest_windows(
                version=ec2.WindowsVersion.WINDOWS_SERVER_2019_ENGLISH_FULL_BASE
            )
            ec2_instance = ec2.Instance(self,
                instance_tag, 
                vpc=vpc,
                instance_type=ec2_instance_type,
                machine_image=ec2_machine_image,
                vpc_subnets=instance_subnet,
                role=role,
                security_group=security_group,
                key_name=config["kp_name"]
                )

            ec2_instance.instance.add_property_override("BlockDeviceMappings", [{
                "DeviceName" : "/dev/xvdb",
                "Ebs" : {
                    "VolumeSize" : "200",
                    "VolumeType" :  "gp2",
                    "DeleteOnTermination" : "true"    
                }},{
                "DeviceName" : "/dev/sda1",
                "Ebs" : {
                    "VolumeSize" : "100",
                    "VolumeType" : "gp2"
                }}
            ])
            
            if instance == "portal_instance":
                logger.info("Found Portal Instance")
                # target_portal = elbv2_targets.InstanceTarget(instance=ec2_instance,port=443)
                target_portal2 = elbv2.InstanceTarget(instance_id=ec2_instance.instance_id, port=443)
                portal_instances.append(target_portal2)
                # target_portal.attach_to_application_target_group(portal_tg)
            if instance == "server_instance" :
                logger.info("Found Server Instance")
                # target_server = elbv2_targets.InstanceTarget(instance=ec2_instance, port=443)
                target_server2 = elbv2.InstanceTarget(instance_id=ec2_instance.instance_id, port=443)
                server_instances.append(target_server2)
                # target_server.attach_to_application_target_group(server_tg)

            
            r53_name = instance_tag.split("_")[1] + instance_tag.split("_")[2]
            record_set = r53.ARecord(self, id=instance_tag + "_rs", target=r53.RecordTarget.from_ip_addresses(ec2_instance.instance_private_ip), zone=r53_phz, record_name=r53_name)
            
        alb = elbv2.ApplicationLoadBalancer(self, config["customer"] + "-" + "arcgis-alb", vpc=vpc, internet_facing=True, security_group=sg_public, load_balancer_name=config["customer"] + "-" + "arcgis-alb")
        portal_tg = elbv2.ApplicationTargetGroup(self, id=config["customer"] + "-portal-tg", target_group_name=config["customer"] + "-portal-tg", port=443, vpc=vpc, target_type=elbv2.TargetType.INSTANCE, targets=portal_instances)
        server_tg = elbv2.ApplicationTargetGroup(self, id=config["customer"] + "-server-tg", target_group_name=config["customer"] + "-server-tg", port=443, vpc=vpc, target_type=elbv2.TargetType.INSTANCE, targets=server_instances)
        listener_cert = elbv2.ListenerCertificate(config["cert_arn"])
        listener = elbv2.ApplicationListener(self, id=config["customer"] +"-listener", load_balancer=alb, certificates=[listener_cert], default_target_groups=[portal_tg], port=443)
        
        zone = r53.HostedZone.from_hosted_zone_attributes(self, "in_hz", zone_name="aws.esri-ps.com", hosted_zone_id=config["public_hosted_zone_id"])
        public_record_set = r53.CnameRecord(self, id="alb_rs", domain_name=alb.load_balancer_dns_name, zone=zone, record_name=config["customer"])