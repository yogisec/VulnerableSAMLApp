import json
import os
import subprocess
from shutil import copyfile


def sp_settings(json_file, sp_ip, idp_ip):
    jsonFile = open(json_file, 'r')
    data = json.load(jsonFile)
    jsonFile.close()

    data['sp']['entityId'] = f'http://{sp_ip}:8000/metadata/'
    data['sp']['assertionConsumerService']['url'] = f'http://{sp_ip}:8000/?acs'
    data['sp']['singleLogoutService']['url'] = f'http://{sp_ip}:8000/?sls'

    data['idp']['entityId'] = f'http://{idp_ip}/simplesamlphp/saml2/idp/metadata.php'
    data['idp']['singleSignOnService']['url'] = f'http://{idp_ip}/simplesamlphp/saml2/idp/SSOService.php'
    data['idp']['singleLogoutService']['url'] = f'http://{idp_ip}/simplesamlphp/saml2/idp/SingleLogoutService.php'

    jsonFile = open(json_file, 'w+')
    jsonFile.write(json.dumps(data, indent=4))
    jsonFile.close()


def idp_settings(settings_file, sp_ip):
    original_text = '127.0.0.1:8000'
    new_text = f'{sp_ip}:8000'

    original_text_blob = open(settings_file).read()
    open(settings_file, 'w').write(original_text_blob.replace(original_text, new_text))


def build_docker(image_build):
    # Builds and runs the docker image defined for the host. 
    
    if image_build == 'idp':
        build = subprocess.Popen(['docker', 'build', '-t', 'idp:1.0', 'vulnerableidp/'])
        build.wait()
        run = subprocess.Popen(['docker', 'run', '-it', '--rm', '--name', 'sp', '-d', '-p', '80:80', 'sp:1.0'])
        run.wait()
        check = subprocess.Popen(['docker', 'ps', '--filter', '--name', 'sp'])
        check.wait()
        print('\n All done run the IDP should be running now.')
        print('To run the image manually after shutting it down use the command below:')
        print(f'\t sudo docker run -it --rm --name {image_build} -d -p 80:80 {image_build}:1.0')
    else:
        build = subprocess.Popen(['docker', 'build', '-t', 'sp:1.0', 'vulnerablesp/'])
        build.wait()
        run = subprocess.Popen(['docker', 'run', '-it', '--rm', '--name', 'sp', '-d', '-p', '8000:8000', 'sp:1.0'])
        run.wait()
        check = subprocess.Popen(['docker', 'ps', '--filter', '--name', 'sp'])
        check.wait()
        print('\n All done the SP image should be running.')
        print('To run the image manually after shutting it down use the command below:')
        print(f'\t sudo docker run -it --rm --name {image_build} -d -p 8000:8000 {image_build}:1.0')


def main():
    # Reset the config files for each run to give people the ability to re-run this if they typo something
    # saves them from having to re-clone repo or edit the files manually

    copyfile('vulnerablesp/yogiSP/saml/settings.original','vulnerablesp/yogiSP/saml/settings.json')
    copyfile('vulnerableidp/saml20-sp-remote.original','vulnerableidp/saml20-sp-remote.php')

    host_config_option = ''
    print(" Begining the configuration process. \n") 

    print('---------------------------------------------')
    print(" Please note that this script is basically doing a find in replace on specific strings that exist in the initial files cloned from the repository.\n If you've already ran this script once and specified different IPs/hostnames for the SP and IDP, there is a strong chance it will not actually update the configuration files for you.\n You should consider manually editing the configuration files or deleteing and re-cloning the repository.")
    print('---------------------------------------------')

    print('\n Which server are we configuring? \n 1 - Identity Prodiver (IDP) \n 2 - Serivce Provider/Web App (SP)')

    while True:
        try:
            host_config_option = int(input('#  '))
            if host_config_option == 1 or host_config_option == 2:
                break
            print('Please enter 1 or 2')
        except Exception as e:
            print('Must be a number')

    while True:
        try:
            docker_direction = input('Do you want to also create and run the Docker image for this host, Y/N? ')
            if docker_direction[0].lower() == 'y' or docker_direction[0].lower() == 'n':
                break
            print('Must be either a Y or N')
        except Exception as e:
            print(f'Must be a Y or N: {e}')

    if docker_direction == 'Y':
        if os.geteuid() != 0:
            sys.exit('Please re-run this script with root privileges if you want to have it build the docker commands for you')

    sp_ip = input('What is the hostname/IP for the SP? ')
    idp_ip = input('What is the hostname/IP for the IDP? ')

    # Configure the Identity Platform (IDP)
    if host_config_option is 1:
        settings_file = 'vulnerableidp/saml20-sp-remote.php'
        idp_settings(settings_file, sp_ip)
        build_docker('idp')

    # Configure the web application / Service Provider (SP)
    elif host_config_option is 2:
        json_file = 'vulnerablesp/yogiSP/saml/settings.json'
        sp_settings(json_file, sp_ip, idp_ip)
        build_docker('sp')

if __name__ == "__main__":
    main()
