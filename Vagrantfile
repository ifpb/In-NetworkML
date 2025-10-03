# -*- mode: ruby -*-
# vi: set ft=ruby :

Vagrant.configure("2") do |config|
  config.vm.box = "bento/debian-12"

  config.vm.provider "virtualbox" do |v|
    v.memory = 1024
    v.cpus = 1
  end

  config.vm.define :s1 do |s|
    s.vm.box = "leandrocalmeida/bmv2-p4"
    s.vm.box_version = "03"
    s.vm.hostname = "s1"

    s.vm.network "private_network", ip: "192.168.56.254"

    s.vm.network "private_network", auto_config: false,
      virtualbox__intnet: "S1-H1"

    s.vm.network "private_network", auto_config: false,
      virtualbox__intnet: "S1-H2"

    s.vm.provider "virtualbox" do |v|
      v.customize ["modifyvm", :id, "--nicpromisc3", "allow-all"]
      v.customize ["modifyvm", :id, "--nicpromisc4", "allow-all"]
    end

    s.vm.provision "ansible" do |ansible|
      ansible.playbook = "./ansible/switch-1.yml"
    end
  end

  # (1..2).reverse_each do |i|
  #   config.vm.define "h#{i}" do |h|
  #     h.vm.hostname = "h#{i}"
  #     h.vm.network "private_network", ip: "192.168.56.#{100+i}", mac: "0800881122#{10+i}",
  #       virtualbox__intnet: "S1-H#{i}"
  #     h.vm.provision "ansible" do |ansible|
  #       ansible.playbook = "./ansible/host-#{i}.yml"
  #     end
  #   end
  # end

  config.vm.define :h1 do |h1|
    h1.vm.hostname = "h1"
    h1.vm.network "private_network", ip: "192.168.56.101", mac: "080088112211",
        virtualbox__intnet: "S1-H1"
    h1.vm.provision "ansible" do |ansible|
      ansible.playbook = "./ansible/host-1.yml"
    end
  end

  config.vm.define :h2 do |h2|

    config.vm.provider "virtualbox" do |v|
      v.memory = 2048
      v.cpus = 4
    end

    h2.vm.hostname = "h2"
    h2.vm.network "private_network", ip: "192.168.56.102", mac: "080088112212",
        virtualbox__intnet: "S1-H2"
    h2.vm.provision "ansible" do |ansible|
      ansible.playbook = "./ansible/host-2.yml"
    end
  end

end
