# {{cookiecutter.role_full_name}}

`{{cookiecutter.role_full_name}}` ansible role

## Example Prompt Inputs

These inputs can be used to create an nginx role using Linuxserver's SWAG image:

```yaml
- name: nginx
  public: true
  template:
    name: {{cookiecutter.container_runtime}}-service
    context:
      container_cap_net_admin: true
      container_repo: lscr.io/linuxserver/swag
      container_tag: latest
      http_port: 80
      https_port: 443
      container_ports:
        _1: "80:80"
        _2: "443:443"
      container_volumes:
        _1:
          src: /config
          dst: /config
        _2:
          src: /data
          dst: /data
      ansible_extra_tasks:
        _1:
          file: _ssl.yaml
          tags: "[nginx, ssl]"
      unix_group_id: 8080
      unix_umask: "002"
      unix_user_id: 8080
```
