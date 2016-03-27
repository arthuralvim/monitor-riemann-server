# -*- mode: ruby -*-
# vi: set ft=ruby :

VAGRANTFILE_API_VERSION = "2"

Vagrant.configure(VAGRANTFILE_API_VERSION) do |config|


    (0..1).each do |i|
        config.vm.define "monitor-#{i}" do |monitor|
            monitor.vm.box = "ubuntu/trusty64"
            monitor.vm.hostname = "monitor-#{i}.dev"
            monitor.vm.network :private_network, ip: "33.33.33.3#{i}"
            monitor.vm.network :forwarded_port, guest: 22, host: 2200 + i, id: 'ssh'
            if i == 0
                monitor.vm.network :forwarded_port, {:guest => 4567, :host => 4567, :id => "dashboard", :auto_correct => true}
                monitor.vm.network :forwarded_port, {:guest => 5555, :host => 5515, :id => "riemann_udp", :protocol => "udp", :auto_correct => true}
                monitor.vm.network :forwarded_port, {:guest => 5555, :host => 5515, :id => "riemann_tcp", :protocol => "tcp", :auto_correct => true}
                monitor.vm.network :forwarded_port, {:guest => 5556, :host => 5516, :id => "riemann_ws", :auto_correct => true}
            end
            monitor.ssh.insert_key = false
        end
    end

    config.vm.provider "virtualbox" do |v|
        v.customize ["modifyvm", :id, "--memory", "512"]
    end

end
