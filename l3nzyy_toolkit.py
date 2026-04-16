#!/usr/bin/env python3
"""
██╗  ██╗ █████╗  ██████╗██╗  ██╗███████╗██████╗     ██╗     ███████╗███╗   ██╗███████╗██╗   ██╗██╗   ██╗
██║  ██║██╔══██╗██╔════╝██║ ██╔╝██╔════╝██╔══██╗    ██║     ██╔════╝████╗  ██║╚══███╔╝╚██╗ ██╔╝╚██╗ ██╔╝
███████║███████║██║     █████╔╝ █████╗  ██████╔╝    ██║     █████╗  ██╔██╗ ██║  ███╔╝  ╚████╔╝  ╚████╔╝ 
██╔══██║██╔══██║██║     ██╔═██╗ ██╔══╝  ██╔══██╗    ██║     ██╔══╝  ██║╚██╗██║ ███╔╝    ╚██╔╝    ╚██╔╝  
██║  ██║██║  ██║╚██████╗██║  ██╗███████╗██║  ██║    ███████╗███████╗██║ ╚████║███████╗   ██║      ██║   
╚═╝  ╚═╝╚═╝  ╚═╝ ╚═════╝╚═╝  ╚═╝╚══════╝╚═╝  ╚═╝    ╚══════╝╚══════╝╚═╝  ╚═══╝╚══════╝   ╚═╝      ╚═╝   
                                                                                                         
        ██╗   ██╗ ██████╗  ██████╗ ██╗     ██╗  ██╗    ██╗   ██╗██╗███╗   ██╗███████╗
        ╚██╗ ██╔╝██╔═══██╗██╔═══██╗██║     ██║ ██╔╝    ██║   ██║██║████╗  ██║██╔════╝
         ╚████╔╝ ██║   ██║██║   ██║██║     █████╔╝     ██║   ██║██║██╔██╗ ██║███████╗
          ╚██╔╝  ██║   ██║██║   ██║██║     ██╔═██╗     ╚██╗ ██╔╝██║██║╚██╗██║╚════██║
           ██║   ╚██████╔╝╚██████╔╝███████╗██║  ██╗     ╚████╔╝ ██║██║ ╚████║███████║
           ╚═╝    ╚═════╝  ╚═════╝ ╚══════╝╚═╝  ╚═╝      ╚═══╝  ╚═╝╚═╝  ╚═══╝╚══════╝
                                                                                     
                    Advanced Information Gathering & Penetration Testing Suite
                              Coded by: L3NZYY | For Educational Use Only
"""

import socket
import requests
import sys
import json
import csv
import threading
import queue
import dns.resolver
import whois
import ssl
import subprocess
import re
import time
import random
import string
from urllib.parse import urlparse, urljoin
from datetime import datetime
from bs4 import BeautifulSoup
import argparse
from colorama import Fore, Back, Style, init

# Initialize colors for terminal
init(autoreset=True)

class HackerL3NZYY:
    def __init__(self, target, threads=50, timeout=3, verbose=False):
        self.target = target.replace('http://', '').replace('https://', '').strip('/')
        self.threads = threads
        self.timeout = timeout
        self.verbose = verbose
        self.start_time = time.time()
        
        # Results storage
        self.results = {
            'tool_name': 'Hacker L3NZYY Tool Kit',
            'version': '2.0',
            'author': 'L3NZYY',
            'target': self.target,
            'scan_time': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'scan_duration': 0,
            'ip_info': {},
            'dns_records': {},
            'whois_data': {},
            'subdomains': [],
            'open_ports': [],
            'web_tech': {},
            'ssl_info': {},
            'directories': [],
            'emails': [],
            'links': [],
            'vulnerabilities': []
        }
        
        # Queues for threading
        self.subdomain_queue = queue.Queue()
        self.port_queue = queue.Queue()
        self.dir_queue = queue.Queue()
        
        # Wordlists
        self.subdomain_wordlist = self._load_subdomain_wordlist()
        self.dir_wordlist = self._load_dir_wordlist()
        
    # ============ BANNER & UI ============
    def show_banner(self):
        """Display the epic L3NZYY banner"""
        banner = f"""
{Fore.WHITE}
                    █
                   ███
                  ██ ██
                 ██   ██
                ██  {Fore.RED}█{Fore.WHITE}   ██
               ██   {Fore.RED}███{Fore.WHITE}   ██
              ██    {Fore.RED}█{Fore.WHITE}     ██
             ██  {Fore.RED}███████{Fore.WHITE}   ██
            ██   {Fore.RED}███████{Fore.WHITE}    ██
           ██    {Fore.RED}██{Fore.WHITE}   {Fore.RED}██{Fore.WHITE}     ██
          ██     {Fore.RED}██{Fore.WHITE}   {Fore.RED}██{Fore.WHITE}      ██
         ██      {Fore.RED}███████{Fore.WHITE}       ██
        ██       {Fore.RED}███████{Fore.WHITE}        ██
       ██         {Fore.RED}███{Fore.WHITE}           ██
      ██            {Fore.RED}█{Fore.WHITE}            ██
     ██                          ██
    ██     [  {Fore.CYAN}HACKER  L3NZYY  {Fore.WHITE}  ]     ██
   ██      [  {Fore.CYAN}TOOL  KIT  v2.0{Fore.WHITE}  ]      ██
  ██       [  {Fore.GREEN}SYSTEM  READY  {Fore.WHITE}  ]       ██
 ██                                     ██
██  {Fore.YELLOW}⚡ Advanced Reconnaissance Suite ⚡{Fore.WHITE}  ██
█{Fore.CYAN}═══════════════════════════════════════{Fore.WHITE}█
{Style.RESET_ALL}
        """
        print(banner)
        
        # Target info box
        box_width = 50
        print(f"{Fore.CYAN}╔{'═' * box_width}╗{Style.RESET_ALL}")
        print(f"{Fore.CYAN}║{Style.RESET_ALL} {Fore.WHITE}TARGET:{Style.RESET_ALL} {Fore.GREEN}{self.target:<35}{Style.RESET_ALL} {Fore.CYAN}║{Style.RESET_ALL}")
        print(f"{Fore.CYAN}║{Style.RESET_ALL} {Fore.WHITE}THREADS:{Style.RESET_ALL} {Fore.GREEN}{self.threads:<34}{Style.RESET_ALL} {Fore.CYAN}║{Style.RESET_ALL}")
        print(f"{Fore.CYAN}║{Style.RESET_ALL} {Fore.WHITE}TIMEOUT:{Style.RESET_ALL} {Fore.GREEN}{self.timeout}s{Fore.WHITE}{' ' * 32}{Style.RESET_ALL} {Fore.CYAN}║{Style.RESET_ALL}")
        print(f"{Fore.CYAN}║{Style.RESET_ALL} {Fore.WHITE}STARTED:{Style.RESET_ALL} {Fore.GREEN}{datetime.now().strftime('%H:%M:%S')}{' ' * 27}{Style.RESET_ALL} {Fore.CYAN}║{Style.RESET_ALL}")
        print(f"{Fore.CYAN}╚{'═' * box_width}╝{Style.RESET_ALL}\n")
        
        # Hacker quote
        quotes = [
            "Access is the beginning, persistence is the art.",
            "In the depths of code, secrets whisper.",
            "Every system has a door; find the key.",
            "Reconnaissance is the soul of penetration.",
            "Information is power, data is weapon."
        ]
        print(f"{Fore.MAGENTA}[*] {random.choice(quotes)}{Style.RESET_ALL}\n")

    def _load_subdomain_wordlist(self):
        """Extended subdomain wordlist"""
        return [
            'www', 'mail', 'ftp', 'localhost', 'webmail', 'smtp', 'pop', 'ns1', 'webdisk',
            'ns2', 'cpanel', 'whm', 'autodiscover', 'autoconfig', 'ns3', 'm', 'imap',
            'test', 'ns', 'blog', 'pop3', 'dev', 'www2', 'admin', 'forum', 'news',
            'vpn', 'ns4', 'www1', 'mail2', 'new', 'mysql', 'old', 'lists', 'support',
            'mobile', 'mx', 'static', 'docs', 'beta', 'shop', 'sql', 'secure', 'demo',
            'cp', 'calendar', 'wiki', 'web', 'media', 'email', 'images', 'img', 'www3',
            'login', 'intranet', 'portal', 'video', 'sip', 'dns2', 'api', 'cdn',
            'stats', 'dns1', 'ns5', 'www4', 'www5', 'mail3', 'staging', 'www6',
            'wp', 'wordpress', 'wp-admin', 'wp-content', 'wp-includes', 'xmlrpc',
            'ssh', 'sftp', 'git', 'svn', 'cvs', 'mercurial', 'hg', 'bazaar', 'bzr',
            'jenkins', 'jira', 'confluence', 'gitlab', 'github', 'bitbucket',
            'docker', 'kubernetes', 'k8s', 'rancher', 'portainer', 'swarm',
            'grafana', 'prometheus', 'kibana', 'elasticsearch', 'logstash',
            'zabbix', 'nagios', 'cacti', 'munin', 'icinga', 'prtg',
            'phpmyadmin', 'pma', 'myadmin', 'mysqladmin', 'dbadmin', 'database',
            'mongo', 'mongodb', 'redis', 'memcached', 'elasticsearch', 'solr',
            'rabbitmq', 'kafka', 'zookeeper', 'hadoop', 'spark', 'storm',
            'backup', 'backups', 'bak', 'old', 'archive', 'archives', 'dump',
            'temp', 'tmp', 'test', 'testing', 'dev', 'devel', 'development',
            'stage', 'staging', 'prod', 'production', 'live', 'uat', 'qa',
            'api-v1', 'api-v2', 'api-v3', 'rest', 'graphql', 'swagger', 'openapi',
            'mobile', 'android', 'ios', 'app', 'apps', 'application', 'client',
            'partner', 'partners', 'vendor', 'vendors', 'supplier', 'suppliers',
            'affiliate', 'affiliates', 'reseller', 'resellers', 'franchise',
            'career', 'careers', 'job', 'jobs', 'employment', 'work', 'join',
            'investor', 'investors', 'ir', 'finance', 'financial', 'invest',
            'press', 'media', 'newsroom', 'pr', 'public', 'relations',
            'corporate', 'corp', 'about', 'story', 'history', 'team', 'leadership',
            'legal', 'privacy', 'policy', 'terms', 'conditions', 'compliance',
            'security', 'sec', 'infosec', 'cyber', 'protect', 'safeguard',
            'status', 'health', 'ping', 'monitor', 'watch', 'observe', 'check',
            'sitemap', 'robots', 'humans', 'ads', 'advertising', 'marketing',
            'analytics', 'stats', 'statistics', 'metrics', 'data', 'report',
            'survey', 'poll', 'vote', 'feedback', 'review', 'rating', 'comment',
            'chat', 'livechat', 'support', 'help', 'desk', 'ticket', 'faq',
            'knowledge', 'base', 'wiki', 'docs', 'documentation', 'manual',
            'guide', 'tutorial', 'course', 'learn', 'training', 'education',
            'academy', 'school', 'university', 'college', 'institute',
            'research', 'lab', 'labs', 'experiment', 'testbed', 'pilot',
            'demo', 'showcase', 'preview', 'alpha', 'beta', 'gamma', 'rc',
            'nightly', 'daily', 'weekly', 'build', 'ci', 'cd', 'pipeline',
            'artifact', 'repo', 'repository', 'source', 'src', 'dist', 'release',
            'download', 'downloads', 'upload', 'uploads', 'file', 'files',
            'share', 'shared', 'public', 'private', 'internal', 'external',
            'cdn', 'static', 'assets', 'asset', 'resource', 'resources',
            'img', 'imgs', 'image', 'images', 'pic', 'pics', 'photo', 'photos',
            'video', 'videos', 'movie', 'movies', 'film', 'films', 'clip', 'clips',
            'audio', 'music', 'song', 'songs', 'podcast', 'radio', 'stream',
            'feed', 'rss', 'atom', 'json', 'xml', 'csv', 'txt', 'pdf', 'doc',
            'search', 'find', 'query', 'lookup', 'browse', 'explorer', 'navigator',
            'map', 'maps', 'direction', 'location', 'place', 'geo', 'gps',
            'weather', 'forecast', 'news', 'update', 'alert', 'notification',
            'event', 'events', 'calendar', 'schedule', 'agenda', 'plan', 'planner',
            'booking', 'reservation', 'order', 'shop', 'store', 'cart', 'checkout',
            'payment', 'pay', 'billing', 'invoice', 'receipt', 'transaction',
            'account', 'accounts', 'user', 'users', 'member', 'members',
            'profile', 'profiles', 'dashboard', 'panel', 'control', 'manage',
            'admin', 'administrator', 'root', 'superuser', 'sudo', 'su',
            'login', 'signin', 'sign', 'auth', 'authenticate', 'oauth', 'sso',
            'register', 'signup', 'join', 'create', 'new', 'start', 'begin',
            'logout', 'signout', 'exit', 'quit', 'leave', 'close', 'end',
            'forgot', 'reset', 'recover', 'restore', 'backup', 'revert',
            'settings', 'config', 'configuration', 'option', 'preference',
            'setup', 'install', 'wizard', 'guide', 'assistant', 'helper',
            'bot', 'robot', 'ai', 'ml', 'nlp', 'assistant', 'agent', 'service',
            'cron', 'crontab', 'scheduler', 'task', 'job', 'worker', 'queue',
            'batch', 'process', 'thread', 'async', 'sync', 'queue', 'stack',
            'cache', 'caching', 'memcache', 'redis', 'varnish', 'squid',
            'proxy', 'proxies', 'gateway', 'bridge', 'tunnel', 'vpn', 'tor',
            'firewall', 'waf', 'ids', 'ips', 'siem', 'soc', 'noc',
            'router', 'switch', 'hub', 'gateway', 'modem', 'accesspoint', 'ap',
            'printer', 'print', 'scanner', 'fax', 'copy', 'device', 'peripheral',
            'iot', 'smart', 'home', 'building', 'office', 'factory', 'plant',
            'sensor', 'actuator', 'controller', 'plc', 'scada', 'ics',
            'drone', 'uav', 'robotics', 'automation', 'machine', 'cnc',
            'server', 'srv', 'host', 'node', 'instance', 'vm', 'container',
            'pod', 'deployment', 'service', 'ingress', 'egress', 'loadbalancer',
            'db', 'database', 'datastore', 'storage', 'disk', 'volume', 'mount',
            'nfs', 'smb', 'cifs', 'afp', 'ftp', 'sftp', 'scp', 'rsync',
            'ldap', 'ad', 'domain', 'dc', 'kerberos', 'ntlm', 'radius', 'tacacs',
            'smtp', 'mail', 'email', 'webmail', 'exchange', 'postfix', 'sendmail',
            'imap', 'pop3', 'pop', 'submission', 'smtps', 'imaps', 'pop3s',
            'xmpp', 'jabber', 'chat', 'irc', 'teamspeak', 'mumble', 'discord',
            'sip', 'voip', 'pbx', 'asterisk', 'freepbx', 'elastix',
            'ntp', 'time', 'clock', 'sync', 'chrony', 'timeserver',
            'dns', 'named', 'bind', 'unbound', 'powerdns', 'dnscrypt',
            'dhcp', 'tftp', 'bootp', 'pxe', 'kickstart', 'preseed',
            'snmp', 'monitoring', 'trap', 'inform', 'poll', 'agent',
            'syslog', 'log', 'logging', 'audit', 'trace', 'debug', 'verbose',
            'netflow', 'sflow', 'ipfix', 'traffic', 'bandwidth', 'usage',
            'cacti', 'nagios', 'zabbix', 'prometheus', 'grafana', 'kibana',
            'splunk', 'elk', 'elastic', 'datadog', 'newrelic', 'appdynamics',
            'pagerduty', 'opsgenie', 'victorops', 'xmatters', 'slack', 'webhook'
        ]

    def _load_dir_wordlist(self):
        """Extended directory wordlist"""
        return [
            'admin', 'administrator', 'adminpanel', 'admincp', 'adm', 'manage', 'management',
            'manager', 'moderator', 'mod', 'webadmin', 'sysadmin', 'root', 'superuser',
            'login', 'signin', 'logout', 'signout', 'register', 'signup', 'createaccount',
            'forgotpassword', 'resetpassword', 'changepassword', 'password', 'pass',
            'auth', 'authentication', 'authorize', 'oauth', 'openid', 'saml', 'sso',
            'api', 'api/v1', 'api/v2', 'api/v3', 'rest', 'graphql', 'swagger', 'openapi',
            'docs', 'documentation', 'doc', 'manual', 'guide', 'help', 'support', 'faq',
            'wp-admin', 'wp-content', 'wp-includes', 'wp-json', 'xmlrpc.php', 'wp-login',
            'wordpress', 'wp', 'drupal', 'joomla', 'magento', 'prestashop', 'opencart',
            'phpmyadmin', 'pma', 'phpmyadmin2', 'phpmyadmin3', 'myadmin', 'mysqladmin',
            'dbadmin', 'database', 'db', 'sql', 'mysql', 'postgresql', 'sqlite', 'oracle',
            'mongo', 'mongodb', 'redis', 'memcached', 'elasticsearch', 'solr', 'couchdb',
            'cassandra', 'neo4j', 'influxdb', 'prometheus', 'timescaledb', 'clickhouse',
            'config', 'configuration', 'conf', 'settings', 'setting', 'env', 'environment',
            'backup', 'backups', 'bak', 'old', 'archive', 'archives', 'dump', 'dumps',
            'temp', 'tmp', 'temporary', 'cache', 'caches', 'log', 'logs', 'logging',
            'test', 'testing', 'tests', 'dev', 'devel', 'development', 'develop',
            'stage', 'staging', 'stg', 'preprod', 'preview', 'demo', 'demonstration',
            'prod', 'production', 'live', 'master', 'main', 'trunk', 'release', 'build',
            'install', 'installation', 'setup', 'wizard', 'configure', 'configurator',
            'update', 'upgrade', 'patch', 'hotfix', 'fix', 'bugfix', 'release', 'version',
            'source', 'src', 'sources', 'code', 'codes', 'script', 'scripts', 'js', 'css',
            'assets', 'asset', 'static', 'resources', 'resource', 'media', 'uploads',
            'upload', 'files', 'file', 'download', 'downloads', 'down', 'get', 'fetch',
            'images', 'image', 'img', 'imgs', 'picture', 'pictures', 'pic', 'pics', 'photo',
            'photos', 'video', 'videos', 'movie', 'movies', 'film', 'films', 'media',
            'audio', 'music', 'sound', 'sounds', 'voice', 'podcast', 'radio', 'stream',
            'content', 'contents', 'data', 'datas', 'dataset', 'datasets', 'database',
            'user', 'users', 'member', 'members', 'account', 'accounts', 'profile',
            'profiles', 'dashboard', 'panel', 'control', 'controlpanel', 'cp', 'usercp',
            'moderatorcp', 'admincp', 'modcp', 'superadmin', 'superuser', 'root',
            'search', 'find', 'query', 'lookup', 'browse', 'explorer', 'navigator',
            'sitemap', 'sitemaps', 'robots.txt', 'humans.txt', 'security.txt', 'ads.txt',
            'crossdomain.xml', 'clientaccesspolicy.xml', 'favicon.ico', 'apple-touch-icon',
            'rss', 'feed', 'feeds', 'atom', 'json', 'xml', 'csv', 'txt', 'pdf', 'doc',
            'secret', 'secrets', 'hidden', 'private', 'internal', 'restricted', 'secure',
            'key', 'keys', 'token', 'tokens', 'credential', 'credentials', 'passwords',
            'passwd', 'htpasswd', 'htaccess', 'htgroup', 'htusers', 'svn', 'git', 'cvs',
            '.git', '.svn', '.hg', '.bzr', '_darcs', '.env', '.env.local', '.env.production',
            'docker', 'docker-compose', 'kubernetes', 'k8s', 'helm', 'chart', 'charts',
            'jenkins', 'gitlab-ci', '.github', 'actions', 'workflows', 'travis', 'circleci',
            'ansible', 'puppet', 'chef', 'salt', 'terraform', 'vagrant', 'packer',
            'nginx', 'apache', 'httpd', 'lighttpd', 'caddy', 'iis', 'tomcat', 'jetty',
            'jboss', 'wildfly', 'weblogic', 'websphere', 'glassfish', 'resin', 'was',
            'php', 'phpinfo', 'php-info', 'info.php', 'pinfo.php', 'i.php', 'test.php',
            'shell', 'cmd', 'command', 'exec', 'execute', 'run', 'eval', 'system',
            'console', 'terminal', 'bash', 'sh', 'zsh', 'fish', 'powershell', 'ps',
            'cgi-bin', 'cgi', 'scripts', 'bin', 'exe', 'executables', 'binary', 'lib',
            'library', 'libraries', 'include', 'includes', 'inc', 'vendor', 'vendors',
            'composer', 'package', 'packages', 'node_modules', 'npm', 'yarn', 'pip',
            'gem', 'bundle', 'cargo', 'maven', 'gradle', 'nuget', 'chocolatey', 'brew',
            'error', 'errors', 'debug', 'debugger', 'trace', 'stacktrace', 'exception',
            'log', 'logs', 'logging', 'logger', 'audit', 'audits', 'report', 'reports',
            'stats', 'statistics', 'metric', 'metrics', 'analytics', 'analytic',
            'monitor', 'monitoring', 'health', 'ping', 'status', 'ready', 'alive',
            'check', 'checks', 'probe', 'probes', 'test', 'tests', 'testing', 'selftest',
            'metrics', 'actuator', 'healthcheck', 'readiness', 'liveness', 'startup',
            'prometheus', 'grafana', 'kibana', 'elasticsearch', 'logstash', 'beats',
            'splunk', 'sumologic', 'datadog', 'newrelic', 'appdynamics', 'dynatrace',
            'pagerduty', 'opsgenie', 'victorops', 'xmatters', 'slack', 'teams', 'discord',
            'webhook', 'webhooks', 'callback', 'callbacks', 'hook', 'hooks', 'event',
            'events', 'trigger', 'triggers', 'action', 'actions', 'workflow', 'workflows',
            'automation', 'automate', 'bot', 'bots', 'robot', 'robots', 'ai', 'ml',
            'cron', 'crontab', 'scheduler', 'schedule', 'job', 'jobs', 'worker', 'workers',
            'queue', 'queues', 'task', 'tasks', 'background', 'async', 'sync', 'batch',
            'process', 'processing', 'thread', 'threads', 'worker', 'workers', 'pool',
            'cache', 'caching', 'memcache', 'memcached', 'redis', 'varnish', 'squid',
            'cdn', 'edge', 'origin', 'source', 'upstream', 'downstream', 'proxy',
            'proxies', 'gateway', 'gateways', 'bridge', 'bridges', 'tunnel', 'tunnels',
            'vpn', 'vpns', 'tor', 'i2p', 'freenet', 'zeronet', 'ipfs', 'dat', 'ssb',
            'firewall', 'waf', 'ids', 'ips', 'siem', 'soc', 'noc', 'honey', 'honeypot',
            'router', 'switch', 'hub', 'gateway', 'modem', 'accesspoint', 'ap', 'wifi',
            'printer', 'printers', 'print', 'scan', 'scanner', 'fax', 'copy', 'device',
            'iot', 'smart', 'home', 'building', 'office', 'factory', 'plant', 'industrial',
            'sensor', 'sensors', 'actuator', 'actuators', 'controller', 'controllers',
            'plc', 'scada', 'ics', 'dcs', 'hmi', 'rtu', 'mtu', 'ied', 'sas', 'fas',
            'drone', 'drones', 'uav', 'uas', 'rpas', 'robot', 'robots', 'robotics',
            'automation', 'automated', 'machine', 'machines', 'cnc', '3dprint', 'lasercut'
        ]

    def print_status(self, message, status='info'):
        """Print formatted status messages"""
        timestamp = datetime.now().strftime('%H:%M:%S')
        if status == 'info':
            print(f"{Fore.CYAN}[{timestamp}] ℹ️  {message}{Style.RESET_ALL}")
        elif status == 'success':
            print(f"{Fore.GREEN}[{timestamp}] ✅ {message}{Style.RESET_ALL}")
        elif status == 'warning':
            print(f"{Fore.YELLOW}[{timestamp}] ⚠️  {message}{Style.RESET_ALL}")
        elif status == 'error':
            print(f"{Fore.RED}[{timestamp}] ❌ {message}{Style.RESET_ALL}")
        elif status == 'hacking':
            print(f"{Fore.MAGENTA}[{timestamp}] 🔥 {message}{Style.RESET_ALL}")
        elif status == 'found':
            print(f"{Fore.GREEN}[{timestamp}] 🎯 FOUND: {message}{Style.RESET_ALL}")

    # ============ MODULE 1: IP & DNS ENUMERATION ============
    def ip_dns_module(self):
        """Comprehensive IP and DNS enumeration"""
        self.print_status("Initializing IP & DNS Reconnaissance Module", 'hacking')
        
        # IP Resolution
        try:
            ipv4 = socket.gethostbyname(self.target)
            self.results['ip_info']['ipv4'] = ipv4
            self.print_status(f"IPv4 Address Resolved: {ipv4}", 'success')
            
            # Reverse DNS
            try:
                reverse = socket.gethostbyaddr(ipv4)
                self.results['ip_info']['reverse_dns'] = reverse[0]
                self.print_status(f"Reverse DNS: {reverse[0]}", 'success')
            except:
                pass
                
            # IPv6
            try:
                ipv6_info = socket.getaddrinfo(self.target, None, socket.AF_INET6)
                if ipv6_info:
                    ipv6 = ipv6_info[0][4][0]
                    self.results['ip_info']['ipv6'] = ipv6
                    self.print_status(f"IPv6 Address: {ipv6}", 'success')
            except:
                pass
                
        except Exception as e:
            self.print_status(f"IP Resolution Failed: {e}", 'error')
            return

        # DNS Records Enumeration
        self.print_status("Enumerating DNS Records...", 'info')
        record_types = ['A', 'AAAA', 'MX', 'NS', 'TXT', 'SOA', 'CNAME', 'PTR', 'SRV', 'CAA', 'DNSKEY', 'DS']
        
        for record in record_types:
            try:
                answers = dns.resolver.resolve(self.target, record)
                records = [str(rdata) for rdata in answers]
                self.results['dns_records'][record] = records
                self.print_status(f"{record} Records: {', '.join(records[:2])}", 'found')
            except:
                pass

    # ============ MODULE 2: WHOIS LOOKUP ============
    def whois_module(self):
        """WHOIS information gathering"""
        self.print_status("Querying WHOIS Database...", 'hacking')
        
        try:
            w = whois.whois(self.target)
            
            self.results['whois_data'] = {
                'domain_name': w.domain_name,
                'registrar': w.registrar,
                'creation_date': str(w.creation_date),
                'expiration_date': str(w.expiration_date),
                'updated_date': str(w.updated_date),
                'name_servers': w.name_servers,
                'status': w.status,
                'emails': w.emails,
                'org': w.org,
                'address': w.address,
                'city': w.city,
                'state': w.state,
                'zipcode': w.zipcode,
                'country': w.country
            }
            
            self.print_status(f"Registrar: {w.registrar}", 'success')
            self.print_status(f"Created: {w.creation_date}", 'success')
            self.print_status(f"Expires: {w.expiration_date}", 'warning')
            self.print_status(f"Organization: {w.org}", 'success')
            
        except Exception as e:
            self.print_status(f"WHOIS Lookup Failed: {e}", 'error')

    # ============ MODULE 3: SUBDOMAIN BRUTE-FORCE ============
    def subdomain_worker(self):
        """Thread worker for subdomain enumeration"""
        while not self.subdomain_queue.empty():
            sub = self.subdomain_queue.get()
            try:
                full_domain = f"{sub}.{self.target}"
                ip = socket.gethostbyname(full_domain)
                
                # Additional check for web server
                try:
                    resp = requests.get(f"http://{full_domain}", timeout=self.timeout, 
                                      headers={'User-Agent': 'Mozilla/5.0'})
                    status = resp.status_code
                except:
                    status = 'N/A'
                
                result = {
                    'subdomain': full_domain,
                    'ip': ip,
                    'http_status': status
                }
                self.results['subdomains'].append(result)
                self.print_status(f"{full_domain} -> {ip} (HTTP: {status})", 'found')
                
            except:
                if self.verbose:
                    self.print_status(f"{sub}.{self.target} - Not Found", 'error')
            finally:
                self.subdomain_queue.task_done()

    def subdomain_module(self):
        """Multi-threaded subdomain enumeration"""
        self.print_status(f"Starting Subdomain Brute-Force ({len(self.subdomain_wordlist)} entries)...", 'hacking')
        
        # Fill queue
        for sub in self.subdomain_wordlist:
            self.subdomain_queue.put(sub)
        
        # Start threads
        threads = []
        for _ in range(min(self.threads, 100)):  # Cap at 100 for subdomains
            t = threading.Thread(target=self.subdomain_worker)
            t.daemon = True
            t.start()
            threads.append(t)
        
        self.subdomain_queue.join()
        self.print_status(f"Found {len(self.results['subdomains'])} subdomains", 'success')

    # ============ MODULE 4: PORT SCANNING ============
    def port_worker(self):
        """Thread worker for port scanning"""
        common_services = {
            21: 'FTP', 22: 'SSH', 23: 'Telnet', 25: 'SMTP', 53: 'DNS', 80: 'HTTP',
            110: 'POP3', 111: 'RPC', 135: 'MSRPC', 139: 'NetBIOS', 143: 'IMAP',
            443: 'HTTPS', 445: 'SMB', 993: 'IMAPS', 995: 'POP3S', 1723: 'PPTP',
            3306: 'MySQL', 3389: 'RDP', 5432: 'PostgreSQL', 5900: 'VNC',
            6379: 'Redis', 8080: 'HTTP-Alt', 8443: 'HTTPS-Alt', 9200: 'Elasticsearch',
            27017: 'MongoDB', 5000: 'Flask', 3000: 'React', 8000: 'Django',
            10000: 'Webmin', 20000: 'Usermin', 9000: 'Portainer', 50000: 'SAP'
        }
        
        while not self.port_queue.empty():
            port = self.port_queue.get()
            try:
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                sock.settimeout(self.timeout)
                result = sock.connect_ex((self.target, port))
                
                if result == 0:
                    service = common_services.get(port, 'Unknown')
                    banner = ''
                    
                    # Try to grab banner
                    try:
                        if port in [21, 22, 25, 110, 143]:
                            banner = sock.recv(1024).decode().strip()
                    except:
                        pass
                    
                    port_info = {
                        'port': port,
                        'service': service,
                        'state': 'open',
                        'banner': banner
                    }
                    self.results['open_ports'].append(port_info)
                    self.print_status(f"Port {port}/{service} OPEN", 'found')
                    
                sock.close()
            except:
                pass
            finally:
                self.port_queue.task_done()

    def port_module(self, custom_ports=None):
        """Multi-threaded port scanner"""
        if custom_ports:
            ports = custom_ports
        else:
            # Extended port list
            ports = [
                21, 22, 23, 25, 53, 80, 81, 110, 111, 113, 135, 139, 143, 179, 199,
                443, 445, 465, 514, 515, 548, 554, 587, 646, 993, 995, 1025, 1026,
                1433, 1720, 1723, 2000, 2001, 3306, 3389, 5060, 5666, 5900, 6001,
                8000, 8008, 8080, 8443, 8888, 10000, 32768, 49152, 49154, 5000,
                3000, 4000, 7000, 9000, 9200, 9300, 5601, 5044, 9600, 27017, 6379,
                5432, 1521, 3307, 8081, 8082, 8083, 8880, 9443, 5001, 8001, 9001,
                10001, 20000, 49153, 49155, 49400, 80, 443, 8080, 8443
            ]
        
        self.print_status(f"Starting Port Scan ({len(ports)} ports)...", 'hacking')
        
        for port in ports:
            self.port_queue.put(port)
        
        threads = []
        for _ in range(min(self.threads, 200)):  # Cap at 200 for ports
            t = threading.Thread(target=self.port_worker)
            t.daemon = True
            t.start()
            threads.append(t)
        
        self.port_queue.join()
        self.print_status(f"Found {len(self.results['open_ports'])} open ports", 'success')

    # ============ MODULE 5: WEB TECHNOLOGY SCAN ============
    def webtech_module(self):
        """Analyze web technologies"""
        self.print_status("Analyzing Web Technologies...", 'hacking')
        
        urls = [f"http://{self.target}", f"https://{self.target}"]
        
        for url in urls:
            try:
                headers = {
                    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/115.0',
                    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
                    'Accept-Language': 'en-US,en;q=0.5',
                    'Accept-Encoding': 'gzip, deflate, br',
                    'Connection': 'keep-alive',
                }
                
                resp = requests.get(url, headers=headers, timeout=self.timeout, 
                                  allow_redirects=True, verify=False)
                
                tech_info = {
                    'url': url,
                    'status_code': resp.status_code,
                    'headers': dict(resp.headers),
                    'technologies': []
                }
                
                # Technology detection
                headers_str = str(resp.headers).lower()
                content = resp.text.lower()
                
                detections = {
                    'WordPress': 'wp-content' in content or 'wordpress' in headers_str,
                    'Drupal': 'drupal' in content or 'drupal' in headers_str,
                    'Joomla': 'joomla' in content,
                    'Magento': 'magento' in content,
                    'Shopify': 'shopify' in content,
                    'Cloudflare': 'cloudflare' in headers_str,
                    'AWS': 'aws' in headers_str or 'amazon' in headers_str,
                    'Apache': 'apache' in headers_str,
                    'Nginx': 'nginx' in headers_str,
                    'IIS': 'iis' in headers_str or 'microsoft' in headers_str,
                    'PHP': 'php' in headers_str or '.php' in content,
                    'ASP.NET': 'asp.net' in headers_str or 'x-aspnet' in headers_str,
                    'jQuery': 'jquery' in content,
                    'React': 'react' in content,
                    'Angular': 'angular' in content,
                    'Vue.js': 'vue' in content,
                    'Bootstrap': 'bootstrap' in content,
                    'Laravel': 'laravel' in content or 'laravel_session' in headers_str,
                    'Django': 'django' in content or 'csrftoken' in headers_str,
                    'Flask': 'flask' in content,
                    'Spring': 'spring' in content,
                    'Express': 'express' in headers_str,
                    'Ruby on Rails': 'rails' in content or 'ruby' in headers_str,
                    'WAF': 'waf' in headers_str or 'firewall' in headers_str,
                    'ModSecurity': 'mod_security' in headers_str,
                    'Imperva': 'imperva' in headers_str,
                    'Sucuri': 'sucuri' in headers_str,
                    'Akamai': 'akamai' in headers_str,
                    'Fastly': 'fastly' in headers_str,
                    'MaxCDN': 'maxcdn' in headers_str,
                    'KeyCDN': 'keycdn' in headers_str
                }
                
                for tech, detected in detections.items():
                    if detected:
                        tech_info['technologies'].append(tech)
                
                self.results['web_tech'][url] = tech_info
                
                self.print_status(f"{url} - Status: {resp.status_code}", 'info')
                self.print_status(f"Server: {resp.headers.get('Server', 'Unknown')}", 'success')
                self.print_status(f"Technologies: {', '.join(tech_info['technologies'][:5])}", 'success')
                
            except Exception as e:
                self.print_status(f"{url} - Error: {e}", 'error')

    # ============ MODULE 6: SSL/TLS ANALYSIS ============
    def ssl_module(self):
        """SSL/TLS certificate analysis"""
        self.print_status("Analyzing SSL/TLS Configuration...", 'hacking')
        
        try:
            import urllib3
            urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
            
            context = ssl.create_default_context()
            context.check_hostname = False
            context.verify_mode = ssl.CERT_NONE
            
            with socket.create_connection((self.target, 443), timeout=self.timeout) as sock:
                with context.wrap_socket(sock, server_hostname=self.target) as ssock:
                    cert = ssock.getpeercert()
                    cipher = ssock.cipher()
                    version = ssock.version()
                    
                    # Check for weak protocols
                    weak_protocols = ['SSLv2', 'SSLv3', 'TLSv1', 'TLSv1.1']
                    is_weak = version in weak_protocols
                    
                    self.results['ssl_info'] = {
                        'subject': cert.get('subject'),
                        'issuer': cert.get('issuer'),
                        'not_after': cert.get('notAfter'),
                        'not_before': cert.get('notBefore'),
                        'serial_number': cert.get('serialNumber'),
                        'tls_version': version,
                        'cipher': cipher,
                        'weak_protocol': is_weak,
                        'alt_names': cert.get('subjectAltName', [])
                    }
                    
                    self.print_status(f"TLS Version: {version}", 'warning' if is_weak else 'success')
                    self.print_status(f"Cipher: {cipher[0]}", 'success')
                    self.print_status(f"Certificate Expires: {cert.get('notAfter')}", 'success')
                    
                    if is_weak:
                        self.print_status("WEAK PROTOCOL DETECTED! Upgrade recommended.", 'warning')
                        self.results['vulnerabilities'].append({
                            'type': 'Weak SSL/TLS',
                            'details': f'Using {version}, upgrade to TLSv1.2+',
                            'severity': 'Medium'
                        })
                    
        except Exception as e:
            self.print_status(f"SSL Analysis Failed: {e}", 'error')

    # ============ MODULE 7: DIRECTORY BRUTE-FORCE ============
    def dir_worker(self):
        """Thread worker for directory brute-forcing"""
        base_urls = [f"http://{self.target}", f"https://{self.target}"]
        
        while not self.dir_queue.empty():
            directory = self.dir_queue.get()
            
            for base_url in base_urls:
                try:
                    url = urljoin(base_url + '/', directory)
                    resp = requests.get(url, timeout=self.timeout, allow_redirects=False,
                                      headers={'User-Agent': 'Mozilla/5.0'})
                    
                    if resp.status_code in [200, 201, 202, 203, 204, 301, 302, 307, 308, 401, 403, 405, 500, 502, 503]:
                        result = {
                            'url': url,
                            'status': resp.status_code,
                            'size': len(resp.content),
                            'redirect': resp.headers.get('Location') if resp.status_code in [301, 302] else None
                        }
                        self.results['directories'].append(result)
                        
                        status_color = 'found' if resp.status_code == 200 else 'warning'
                        self.print_status(f"[{resp.status_code}] {url} ({len(resp.content)} bytes)", status_color)
                        
                except:
                    pass
            self.dir_queue.task_done()

    def directory_module(self):
        """Directory brute-forcing"""
        self.print_status(f"Starting Directory Brute-Force ({len(self.dir_wordlist)} entries)...", 'hacking')
        
        for directory in self.dir_wordlist:
            self.dir_queue.put(directory)
        
        threads = []
        for _ in range(min(self.threads, 50)):  # Cap at 50 for directories
            t = threading.Thread(target=self.dir_worker)
            t.daemon = True
            t.start()
            threads.append(t)
        
        self.dir_queue.join()
        self.print_status(f"Found {len(self.results['directories'])} interesting paths", 'success')

    # ============ MODULE 8: EMAIL HARVESTING ============
    def email_module(self):
        """Harvest emails from website"""
        self.print_status("Harvesting Email Addresses...", 'hacking')
        
        try:
            urls_to_check = [f"http://{self.target}", f"https://{self.target}"]
            all_emails = set()
            
            for url in urls_to_check:
                try:
                    resp = requests.get(url, timeout=self.timeout, headers={'User-Agent': 'Mozilla/5.0'})
                    
                    # Regex for email extraction
                    email_pattern = r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}'
                    emails = re.findall(email_pattern, resp.text)
                    
                    # Filter out common false positives
                    invalid_patterns = ['.png', '.jpg', '.gif', '.css', '.js', 'example.com', 'domain.com', 'email.com']
                    for email in emails:
                        if not any(pattern in email.lower() for pattern in invalid_patterns):
                            all_emails.add(email)
                    
                    # Check common pages
                    common_pages = ['/contact', '/about', '/team', '/staff', '/careers', '/support']
                    for page in common_pages:
                        try:
                            page_resp = requests.get(urljoin(url, page), timeout=self.timeout, 
                                                   headers={'User-Agent': 'Mozilla/5.0'})
                            page_emails = re.findall(email_pattern, page_resp.text)
                            for email in page_emails:
                                if not any(pattern in email.lower() for pattern in invalid_patterns):
                                    all_emails.add(email)
                        except:
                            pass
                            
                except:
                    pass
            
            self.results['emails'] = list(all_emails)
            
            for email in list(all_emails)[:10]:  # Show first 10
                self.print_status(email, 'found')
                
            if len(all_emails) > 10:
                self.print_status(f"... and {len(all_emails) - 10} more", 'info')
                
        except Exception as e:
            self.print_status(f"Email Harvesting Failed: {e}", 'error')

    # ============ MODULE 9: VULNERABILITY CHECKS ============
    def vuln_check_module(self):
        """Basic vulnerability checks"""
        self.print_status("Running Basic Vulnerability Checks...", 'hacking')
        
        # Check for common files
        sensitive_files = [
            '/.env', '/.git/config', '/.htaccess', '/.htpasswd',
            '/config.php', '/config.inc.php', '/wp-config.php',
            '/phpinfo.php', '/info.php', '/.DS_Store',
            '/robots.txt', '/sitemap.xml', '/crossdomain.xml',
            '/server-status', '/server-info', '/status', '/phpmyadmin'
        ]
        
        base_url = f"http://{self.target}"
        
        for file_path in sensitive_files:
            try:
                url = base_url + file_path
                resp = requests.get(url, timeout=self.timeout, allow_redirects=False,
                                  headers={'User-Agent': 'Mozilla/5.0'})
                
                if resp.status_code == 200:
                    self.results['vulnerabilities'].append({
                        'type': 'Exposed Sensitive File',
                        'url': url,
                        'details': f'{file_path} is accessible',
                        'severity': 'High' if file_path in ['/.env', '/.git/config', '/wp-config.php'] else 'Medium'
                    })
                    self.print_status(f"CRITICAL: {file_path} exposed!", 'error')
                    
            except:
                pass
        
        # Check security headers
        try:
            resp = requests.get(base_url, timeout=self.timeout, headers={'User-Agent': 'Mozilla/5.0'})
            security_headers = ['X-Frame-Options', 'X-Content-Type-Options', 'X-XSS-Protection',
                              'Strict-Transport-Security', 'Content-Security-Policy', 'Referrer-Policy']
            
            missing_headers = []
            for header in security_headers:
                if header not in resp.headers:
                    missing_headers.append(header)
            
            if missing_headers:
                self.results['vulnerabilities'].append({
                    'type': 'Missing Security Headers',
                    'details': f'Missing: {", ".join(missing_headers)}',
                    'severity': 'Low'
                })
                self.print_status(f"Missing Security Headers: {', '.join(missing_headers[:3])}", 'warning')
                
        except:
            pass

    # ============ SAVE RESULTS ============
    def save_results(self, output_dir='./output'):
        """Save results in multiple formats"""
        import os
        os.makedirs(output_dir, exist_ok=True)
        
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        base_filename = f"{output_dir}/{self.target}_{timestamp}"
        
        # JSON Export
        json_file = f"{base_filename}.json"
        with open(json_file, 'w') as f:
            json.dump(self.results, f, indent=4, default=str)
        self.print_status(f"Results saved to {json_file}", 'success')
        
        # CSV Export (summary)
        csv_file = f"{base_filename}.csv"
        with open(csv_file, 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(['Category', 'Finding', 'Details'])
            
            # IP Info
            writer.writerow(['IP', 'IPv4', self.results['ip_info'].get('ipv4', 'N/A')])
            
            # Open Ports
            for port in self.results['open_ports']:
                writer.writerow(['Port', f"{port['port']}/{port['service']}", 'Open'])
            
            # Subdomains
            for sub in self.results['subdomains']:
                writer.writerow(['Subdomain', sub['subdomain'], sub['ip']])
            
            # Directories
            for dir_info in self.results['directories']:
                writer.writerow(['Directory', dir_info['url'], f"Status: {dir_info['status']}"])
            
            # Vulnerabilities
            for vuln in self.results['vulnerabilities']:
                writer.writerow(['Vulnerability', vuln['type'], f"{vuln['details']} (Severity: {vuln['severity']})"])
        
        self.print_status(f"CSV saved to {csv_file}", 'success')
        
        # Text Report
        txt_file = f"{base_filename}_report.txt"
        with open(txt_file, 'w') as f:
            f.write(f"HACKER L3NZYY TOOL KIT - RECONNAISSANCE REPORT\n")
            f.write(f"{'='*60}\\n\\n")
            f.write(f"Target: {self.target}\\n")
            f.write(f"Scan Date: {self.results['scan_time']}\\n")
            f.write(f"Scan Duration: {self.results['scan_duration']:.2f} seconds\\n\\n")
            
            f.write(f"IP INFORMATION\\n{'-'*30}\\n")
            for key, value in self.results['ip_info'].items():
                f.write(f"{key}: {value}\\n")
            
            f.write(f"\\nOPEN PORTS\\n{'-'*30}\\n")
            for port in self.results['open_ports']:
                f.write(f"{port['port']}/{port['service']} - {port['state']}\\n")
            
            f.write(f"\\nSUBDOMAINS ({len(self.results['subdomains'])} found)\\n{'-'*30}\\n")
            for sub in self.results['subdomains'][:20]:  # First 20
                f.write(f"{sub['subdomain']} -> {sub['ip']}\\n")
            
            f.write(f"\\nVULNERABILITIES ({len(self.results['vulnerabilities'])} found)\\n{'-'*30}\\n")
            for vuln in self.results['vulnerabilities']:
                f.write(f"[{vuln['severity']}] {vuln['type']}: {vuln['details']}\\n")
        
        self.print_status(f"Text report saved to {txt_file}", 'success')
        
        return base_filename

    # ============ MAIN EXECUTION ============
    def run(self, modules=None):
        """Execute all or selected modules"""
        self.show_banner()
        
        if modules is None:
            modules = ['all']
        
        # Core modules (always run)
        self.ip_dns_module()
        
        # Optional modules
        if 'all' in modules or 'whois' in modules:
            self.whois_module()
        
        if 'all' in modules or 'subdomains' in modules:
            self.subdomain_module()
        
        if 'all' in modules or 'ports' in modules:
            self.port_module()
        
        if 'all' in modules or 'web' in modules:
            self.webtech_module()
        
        if 'all' in modules or 'ssl' in modules:
            self.ssl_module()
        
        if 'all' in modules or 'dirs' in modules:
            self.directory_module()
        
        if 'all' in modules or 'emails' in modules:
            self.email_module()
        
        if 'all' in modules or 'vulns' in modules:
            self.vuln_check_module()
        
        # Calculate duration
        self.results['scan_duration'] = time.time() - self.start_time
        
        # Final summary
        print(f"\n{Fore.CYAN}{'='*60}{Style.RESET_ALL}")
        self.print_status("SCAN COMPLETE - SUMMARY", 'hacking')
        print(f"{Fore.CYAN}{'='*60}{Style.RESET_ALL}")
        
        print(f"{Fore.GREEN}Target: {self.target}{Style.RESET_ALL}")
        print(f"{Fore.GREEN}Duration: {self.results['scan_duration']:.2f} seconds{Style.RESET_ALL}")
        print(f"{Fore.GREEN}Subdomains Found: {len(self.results['subdomains'])}{Style.RESET_ALL}")
        print(f"{Fore.GREEN}Open Ports: {len(self.results['open_ports'])}{Style.RESET_ALL}")
        print(f"{Fore.GREEN}Directories Found: {len(self.results['directories'])}{Style.RESET_ALL}")
        print(f"{Fore.GREEN}Emails Harvested: {len(self.results['emails'])}{Style.RESET_ALL}")
        print(f"{Fore.RED if self.results['vulnerabilities'] else Fore.GREEN}Vulnerabilities: {len(self.results['vulnerabilities'])}{Style.RESET_ALL}")
        
        # Save results
        output_path = self.save_results()
        
        print(f"\n{Fore.MAGENTA}[*] All data saved to: {output_path}*.{Style.RESET_ALL}")
        print(f"{Fore.MAGENTA}[*] Use this information responsibly and legally!{Style.RESET_ALL}")
        print(f"{Fore.CYAN}{'='*60}{Style.RESET_ALL}\n")
        
        return self.results

def main():
    parser = argparse.ArgumentParser(
        description='Hacker L3NZYY Tool Kit - Advanced Reconnaissance Suite',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=f'''
{Fore.CYAN}Examples:{Style.RESET_ALL}
  python3 l3nzyy_toolkit.py target.com
  python3 l3nzyy_toolkit.py target.com -t 100 -o ./results
  python3 l3nzyy_toolkit.py target.com -m ports web vulns
  python3 l3nzyy_toolkit.py target.com --threads 200 --timeout 5 -v

{Fore.CYAN}Modules:{Style.RESET_ALL}
  all         Run all modules (default)
  whois       WHOIS lookup
  subdomains  Subdomain enumeration
  ports       Port scanning
  web         Web technology detection
  ssl         SSL/TLS analysis
  dirs        Directory brute-force
  emails      Email harvesting
  vulns       Vulnerability checks
        '''
    )
    
    parser.add_argument('target', help='Target domain to scan')
    parser.add_argument('-t', '--threads', type=int, default=50, 
                       help='Number of threads (default: 50, max: 200)')
    parser.add_argument('--timeout', type=int, default=3,
                       help='Request timeout in seconds (default: 3)')
    parser.add_argument('-o', '--output', default='./output',
                       help='Output directory (default: ./output)')
    parser.add_argument('-m', '--modules', nargs='+', 
                       choices=['all', 'whois', 'subdomains', 'ports', 'web', 'ssl', 'dirs', 'emails', 'vulns'],
                       default=['all'],
                       help='Modules to run (default: all)')
    parser.add_argument('-v', '--verbose', action='store_true',
                       help='Enable verbose output')
    parser.add_argument('--ports', nargs='+', type=int,
                       help='Custom ports to scan (e.g., --ports 80 443 8080)')
    
    args = parser.parse_args()
    
    # Validate threads
    threads = min(args.threads, 200)
    
    # Initialize and run
    tool = HackerL3NZYY(args.target, threads=threads, timeout=args.timeout, verbose=args.verbose)
    
    try:
        results = tool.run(modules=args.modules)
    except KeyboardInterrupt:
        print(f"\n{Fore.RED}[!] Scan interrupted by user{Style.RESET_ALL}")
        sys.exit(1)

if __name__ == "__main__":
    main()
