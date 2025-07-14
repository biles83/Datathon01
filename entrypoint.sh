#!/bin/bash
# Iniciar o supervisor que vai manter todos os serviços no ar
exec supervisord -c /etc/supervisord.conf