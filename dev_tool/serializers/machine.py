from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from dev_tool.models import Services
from paramiko import ssh_exception
import paramiko


class MachineSessionSer(serializers.ModelSerializer):
    alias = serializers.CharField(allow_blank=True)

    class Meta:
        model = Services
        fields = '__all__'

    def validate(self, attrs):
        """验证会话信息是否可使用"""
        host = attrs.get('host')
        username = attrs.get('username')
        password = attrs.get('password')
        cli = paramiko.SSHClient()
        cli.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        try:
            cli.connect(
                hostname=host,
                username=username,
                password=password
            )
            cli.close()

        except ssh_exception.NoValidConnectionsError:
            raise ValidationError('未找到该主机ip')
        except ssh_exception.AuthenticationException:
            raise ValidationError('主机用户登录认证无法通过')
        except Exception as e:
            raise ValidationError('设备连接错误:' + str(e))
        return attrs


class MachineSessionListSer(serializers.Serializer):
    id = serializers.IntegerField()
    host = serializers.CharField()
    alias = serializers.CharField()

