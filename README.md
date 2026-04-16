
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
 
# L3nzyy Toolkit

## 🚀 Setup

```bash
sudo apt update && sudo apt upgrade -y

sudo apt install python3 python3-pip python3-venv -y

cd ~/l3nzyy-toolkit

python3 -m venv venv

source venv/bin/activate

pip install dnspython requests colorama beautifulsoup4 python-whois

sudo apt install whois dnsutils nmap -y

git clone https://github.com/hacker1000119-cmd/l3nzyy-toolkit.git
cd l3nzyy-toolkit

pip3 install requests beautifulsoup4 colorama dnspython python-whois

chmod +x l3nzyy_toolkit.py

sudo ln -s ~/l3nzyy-toolkit/l3nzyy_toolkit.py /usr/local/bin/l3nzyy

## USAGE

l3nzyy --help
l3nzyy example.com
l3nzyy example.com -t 100 --timeout 5 -v
l3nzyy example.com -m ports web vulns
