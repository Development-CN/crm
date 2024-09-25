cd C:\inetpub\wwwroot\Nuevo_crm_Madiautos\crm
call .\newenv\scripts\activate
call daphne -b 201.150.44.27 -p 5023 crm.asgi:application
