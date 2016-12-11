username = node['ssh_user']['name']
ssh_filename = node['ssh_user']['ssh_filename']

# setup ssh server
package 'openssh-server'

# be explicit and enable ssh server
service "ssh" do
    action [:start, :enable]
end

# create /etc/ssh in case home dir is encrypted
directory "/etc/ssh/#{username}" do
    owner "#{username}"
    group "#{username}"
    action :create
    mode '0700'
end

# setup authorized keys
cookbook_file "/home/#{username}/.ssh/authorized_keys" do
    source "authorized_keys/#{username}.keys"
    owner "#{username}"
    group "#{username}"
    action :create_if_missing
    mode '0600'
end

# update the config - mainly to disable password login
# and replace authorized key paths
cookbook_file "/etc/ssh/sshd_config"
    source 'sshd_config'
    owner 'root'
    group 'root'
    mode '0600'
    action :create
    notifies :restart, "service[ssh]"
end
