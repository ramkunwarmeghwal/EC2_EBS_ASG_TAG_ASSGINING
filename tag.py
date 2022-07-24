import boto3

def ec2(event, context):
    ec2_client = boto3.client("ec2")
    response = ec2_client.describe_instances() 
    instances = response['Reservations']

    InstanceId = []
    for instance in  instances:
        if (instance['Instances'][0]['Tags'][0]['Value'])=='':
            print("add tag")
            InstanceId.append(instance['Instances'][0]['InstanceId'])
        #else:
         #   print(instance['Instances'][0]['Tags'][0]['Value'])

    tag_creation = ec2_client.create_tags(
    Resources = InstanceId,
       Tags=[
            {
                'Key': 'string',
                'Value': 'tag-1'
            },
          ]
       )
    
    
    
def ebs(event, context):
    ec2 = boto3.resource('ec2')
    for instance in ec2.instances.all():
        print ('instance:', instance)
        ec2tags = instance.tags
        print ('tags:', ec2tags)
        for volume in instance.volumes.all():
            print ('volume:', volume)
#           Create tags on volume if they don't match the instance
            if volume.tags != ec2tags:
                print('\033[93m' + 'Tags don\'t match, updating')
                volume.create_tags(DryRun=False, Tags=ec2tags)
            print ('tags:', volume.tags)
            return(volume.tags)
            
def asg(event,context):
    # add tag ASG which have no tag
        client = boto3.client('autoscaling')
        tags = client.describe_tags()

        asg_id = []
        if tags['Tags'][0]['Value']=='':
                print("add tag")
                asg_id.append(tags['Tags'][0]['ResourceId'])
        else:
                print(tags['Tags'][0]['Value'])

       #for i in asg_id:    
       tag_creation = client.create_or_update_tags(
       Tags=[
            {
                'ResourceId': 'asg',
                'ResourceType': 'auto-scaling-group',
                'Key': 'Name',
                'Value': 'asg-tag',
                'PropagateAtLaunch': True|False
            },
          ]
       )

    tags = client.describe_tags()
    return(tags['Tags'])
