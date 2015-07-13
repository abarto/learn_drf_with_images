# -*- mode: ruby -*-
# vi: set ft=ruby :

# All Vagrant configuration is done below. The "2" in Vagrant.configure
# configures the configuration version (we support older styles for
# backwards compatibility). Please don't change it unless you know what
# you're doing.
Vagrant.configure(2) do |config|
  # The most common configuration options are documented and commented below.
  # For a complete reference, please see the online documentation at
  # https://docs.vagrantup.com.

  # Every Vagrant development environment requires a box. You can search for
  # boxes at https://atlas.hashicorp.com/search.
  config.vm.box = "ubuntu/trusty64"

  config.vm.hostname = "learn-drf-with-images.local"

  # Disable automatic box update checking. If you disable this, then
  # boxes will only be checked for updates when the user runs
  # `vagrant box outdated`. This is not recommended.
  # config.vm.box_check_update = false

  # Create a forwarded port mapping which allows access to a specific port
  # within the machine from a port on the host machine. In the example below,
  # accessing "localhost:8080" will access port 80 on the guest machine.
  # config.vm.network "forwarded_port", guest: 80, host: 8080

  config.vm.network "forwarded_port", guest: 80, host: 8000

  # Create a private network, which allows host-only access to the machine
  # using a specific IP.
  # config.vm.network "private_network", ip: "192.168.33.10"

  # Create a public network, which generally matched to bridged network.
  # Bridged networks make the machine appear as another physical device on
  # your network.
  # config.vm.network "public_network"

  # Share an additional folder to the guest VM. The first argument is
  # the path on the host to the actual folder. The second argument is
  # the path on the guest to mount the folder. And the optional third
  # argument is a set of non-required options.
  # config.vm.synced_folder "../data", "/vagrant_data"

  config.vm.synced_folder ".", "/home/vagrant/learn_drf_with_images/"

  # Provider-specific configuration so you can fine-tune various
  # backing providers for Vagrant. These expose provider-specific options.
  # Example for VirtualBox:
  #
  # config.vm.provider "virtualbox" do |vb|
  #   # Display the VirtualBox GUI when booting the machine
  #   vb.gui = true
  #
  #   # Customize the amount of memory on the VM:
  #   vb.memory = "1024"
  # end
  #
  # View the documentation for the provider you are using for more
  # information on available options.

  config.vm.provider "virtualbox" do |vb|
    vb.memory = "1024"
  end

  # Define a Vagrant Push strategy for pushing to Atlas. Other push strategies
  # such as FTP and Heroku are also available. See the documentation at
  # https://docs.vagrantup.com/v2/push/atlas.html for more information.
  # config.push.define "atlas" do |push|
  #   push.app = "YOUR_ATLAS_USERNAME/YOUR_APPLICATION_NAME"
  # end

  # Enable provisioning with a shell script. Additional provisioners such as
  # Puppet, Chef, Ansible, Salt, and Docker are also available. Please see the
  # documentation for more information about their specific syntax and use.
  # config.vm.provision "shell", inline: <<-SHELL
  #   sudo apt-get update
  #   sudo apt-get install -y apache2
  # SHELL

  config.vm.provision "shell", inline: <<-SHELL
    apt-get update
    apt-get install -y python3 python3-dev postgresql postgresql-server-dev-all nginx

    sudo -u postgres psql --command="CREATE USER learn_drf_with_images WITH PASSWORD 'learn_drf_with_images';"
    sudo -u postgres psql --command="CREATE DATABASE learn_drf_with_images WITH OWNER learn_drf_with_images;"
    sudo -u postgres psql --command="GRANT ALL PRIVILEGES ON DATABASE learn_drf_with_images TO learn_drf_with_images;"

    echo '
# learn_drf_with_images.conf

upstream django {
  server 127.0.0.1:8000;
}

server {
  listen      80;
  server_name 127.0.0.1 localhost learn-drf-with-images learn-drf-with-images.local;
  charset     utf-8;

  client_max_body_size 75M;   # adjust to taste

  location /media  {
      alias /home/vagrant/learn_drf_with_images/learn_drf_with_images/media;
  }

  location /static {
      alias /home/vagrant/learn_drf_with_images/learn_drf_with_images/static;
  }

  location / {
      proxy_pass       http://django;
      proxy_redirect   off;
      proxy_set_header Host $host;
      proxy_set_header X-Real-IP $remote_addr;
      proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
      proxy_set_header X-Forwarded-Host $server_name:8000;
  }
}
    ' > /etc/nginx/conf.d/learn_drf_with_images.conf

    service nginx reload
  SHELL

  config.vm.provision "shell", privileged: false, inline: <<-SHELL
    pyvenv-3.4 --without-pip learn_drf_with_images_venv
    source learn_drf_with_images_venv/bin/activate
    curl --silent --show-error --retry 5 https://bootstrap.pypa.io/get-pip.py | python

    pip install -r learn_drf_with_images/requirements.txt

    cd learn_drf_with_images/learn_drf_with_images/

    python manage.py migrate

    echo '
    [
    {
        "fields": {
            "password": "pbkdf2_sha256$20000$fUZfRXo5pI0X$uq5/DUsH4ArHdhr5Dv0gfKauW6HMrX4o3ANE5d7sois=",
            "user_permissions": [],
            "is_staff": true,
            "username": "admin",
            "email": "vagrant@learn-drf-with-images.local",
            "groups": [],
            "last_name": "",
            "date_joined": "2015-07-08T00:22:51.199Z",
            "is_superuser": true,
            "is_active": true,
            "last_login": "2015-07-08T00:51:46.558Z",
            "first_name": ""
        },
        "model": "auth.user",
        "pk": 1
    },
    {
        "fields": {
            "password": "pbkdf2_sha256$20000$FUn3mhnbQNHz$SDYMXBmFNOcT/tKK6Xq162M8PoWv+ox3YsplPD8OWeI=",
            "user_permissions": [],
            "is_staff": false,
            "username": "user1",
            "email": "john.doe@learn-drf-with-images.local",
            "groups": [],
            "last_name": "Doe",
            "date_joined": "2015-07-08T00:52:05Z",
            "is_superuser": false,
            "is_active": true,
            "last_login": null,
            "first_name": "John"
        },
        "model": "auth.user",
        "pk": 2
    },
    {
        "fields": {
            "password": "pbkdf2_sha256$20000$IZ3WijqqoQQA$kszc9d98228H9Gkl/Ar64Sst2UVkrweA45TxUubgdPQ=",
            "user_permissions": [],
            "is_staff": false,
            "username": "user2",
            "email": "jane.doe@learn-drf-with-images.local",
            "groups": [],
            "last_name": "Doe",
            "date_joined": "2015-07-08T00:53:06Z",
            "is_superuser": false,
            "is_active": true,
            "last_login": null,
            "first_name": "Jane"
        },
        "model": "auth.user",
        "pk": 3
    },
    {
        "fields": {
            "image": "",
            "date_of_birth": "1980-01-01",
            "phone_number": null,
            "gender": "M"
        },
        "model": "user_profiles.userprofile",
        "pk": 2
    },
    {
        "fields": {
            "image": "",
            "date_of_birth": "1990-01-01",
            "phone_number": null,
            "gender": "F"
        },
        "model": "user_profiles.userprofile",
        "pk": 3
    },
    {
        "fields": {
            "name": "learn_drf_with_images_app",
            "client_secret": "QvnnGqhylppTVVAUvmAnqOTKBSrj4rKMDAnZPg90aafyOmtBrNUfb43ngn0thE2kzasm0tJ8NdozsXM25tmNTzlpM2zPB1hCJPMQHt7bfdLwdZM7yRS71fcJSVA6IBsN",
            "client_id": "zmfZyf7EAGJJ6imph3qtwGtoH8eqt1VdVmRZh7NC",
            "authorization_grant_type": "password",
            "skip_authorization": true,
            "redirect_uris": "",
            "user": [
                "admin"
            ],
            "client_type": "public"
        },
        "model": "oauth2_provider.application",
        "pk": 1
    }
    ]
    ' > data.json

    python manage.py loaddata data.json
    python manage.py collectstatic --noinput
  SHELL

  config.vm.provision "shell", run: "always", privileged: false, inline: <<-SHELL
    source /home/vagrant/learn_drf_with_images_venv/bin/activate

    cd /home/vagrant/learn_drf_with_images/learn_drf_with_images

    gunicorn --bind 127.0.0.1:8000 --daemon --workers 4 learn_drf_with_images.wsgi
  SHELL
end
