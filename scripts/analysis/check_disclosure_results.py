import os
import re
import sys
import time
import logging
import pandas as pd

from urllib.parse import urlparse
from typing import List, Dict, Tuple
from datetime import datetime
from github import Github, GithubException, Auth
from scripts import GITHUB_TOKENS


REPORTED_REPOS = """
https://github.com/angelita89hoppezjd/WondershareFilmora
https://github.com/Casko00/wallet-stealer
https://github.com/Cinoquloqaz1267ibanu/minecraftBFH
https://github.com/CryptoRig-Optimizer-Maximize-Profits/.github
https://github.com/DarkMod3/CMSP-Plataformas-Hacks
https://github.com/Di3colearn/Active-Developer-Badge
https://github.com/dinosaur93702/Hypixel-SkyBlock
https://github.com/duckdunk/Genshin-Impact
https://github.com/ellen-james77/Office
https://github.com/Ethrunner1/Ethrunner-Sniper-bot
https://github.com/rexidtc/Blackswipe-Dumps
https://github.com/iexa/justexp
https://github.com/ILurch/UzaProject
https://github.com/jayyagain/Adobe-Animate
https://github.com/jokmandis/Proxy-v1.2
https://github.com/Kalxi/Rewind-AI-WQA
https://github.com/Ke14523sufu/VALORANTBLACK
https://github.com/Levoerly/lovel-533313
https://github.com/lorstoki/Lis
https://github.com/masonlewisx1/Pekka-Android-rat-2024
https://github.com/MircaLor/genshin-impact-cheat
https://github.com/Propants05/swot
https://github.com/pyno567402/ua5vkyr8
https://github.com/Rtyn1337/Thimble-bot-4.1
https://github.com/rukhsar88/dotcoin-autoclicker
https://github.com/Sepehr0Day/Cubes-auto-bot
https://github.com/sflimbusfisufzs/wisper
https://github.com/shahadatofficial10/raygun-fivem-cheats
https://github.com/SniperDev00001/PumpFun-Sniper-Bot
https://github.com/swerunanp/Coman
https://github.com/syedSUBHAN-SALEEM/Catizen-aut0
https://github.com/Synthmania/StakeBot-Predictor
https://github.com/TeddyCSoftware/DEX-JavaScript-Front-Running-Bot-V4-TeddyCSoftware
https://github.com/villanitaorlando416/sakurabestgitsoft
https://github.com/weesehellopeopl93/erjng
https://github.com/x1nx1n8023/hwidspoof
https://github.com/AbdelrahmanDyaa/To-do-App
https://github.com/andreamaggi111/andreamaggi1111
https://github.com/deimeifei/Rust-HCK-2024
https://github.com/ZizouX0/ZizouX01
https://github.com/Yourmomshamster/discord-bot
https://github.com/lluanlima/lnternet-DownIoad-Manager-2024-IDM-free
https://github.com/WILLAS-NASCIMENTO/WILLAS-NASCIMENTO1
https://github.com/weeqeerulesinpage7/drhea
https://github.com/waynelopd/retjkgn
https://github.com/warqutra1992/ejrgwe
https://github.com/virtuallordsniper973/eirbgn
https://github.com/virgonessa30/thesakura
https://github.com/FilimonServer/Adobe-After-Effects-2025
https://github.com/vertyxanwall1992/sakurabest
https://github.com/urchalexktank308/asakura
https://github.com/uffmeet1992/sakura1104
https://github.com/Lolipapss/laughing-disco
https://github.com/touhid9teen/ReactifyLab
https://github.com/L3MO1337/Thimble-Exploit-Bot-4.0
https://github.com/hanachaari/Rust-hck2024
https://github.com/rsdh/Nexus-Roblox
https://github.com/quangquanxdvnn/psychic-adventure
https://github.com/papdji/Ai-Aimbot-For-PC
https://github.com/NirvanaSNM/NirvanaSNM1
https://github.com/loneans771/Adobe-illustrator-cc-free
https://github.com/khizzcr7/ExternalFortnite
https://github.com/Kimmel-Sistemas/Kimmel-Sistemas1
https://github.com/kirankumar5522/Generator-of-Wallets-
https://github.com/kjart-alt/fuzzy-winner
https://github.com/Lolipapss/solid-octo-succotash
https://github.com/Atiq0629/seed-phrase-generator
https://github.com/BeurStma/Trovo-ViewBot
https://github.com/6cikukivunu/Warzone2BFH
https://github.com/williamcorrea23/boolfamily-autoclicker
https://github.com/Uttampatel1/temp1
https://github.com/Tus6224ysama/7ev7vs9dbnfs6
https://github.com/Sopygi8282v/fifaBLACK
https://github.com/Rabajysebe/udoha
https://github.com/misteraff/metaland-autoclicker
https://github.com/memicamina/MMproBump-autoclicker
https://github.com/Memahepikab/escapefromtarkovBLACK
https://github.com/lEMuj1uQyNEtuGUzETyQ/ApexlegendsBLACK
https://github.com/50yearskippur/Facebook-Bot2024
https://github.com/alves-py/Controle_Financeiro
https://github.com/arion4736/AutoCAD
https://github.com/BearAnBull/Pancakeswap-Prediction-Winningbot
https://github.com/hUSiXOvy57852lugoR/Destiny2BLACK
https://github.com/beqoni7WUkoVYwu/dbdBFH
https://github.com/GFLucas/black-myth-wukong
https://github.com/iokolol/iokol-proj
https://github.com/JesusAv01/YT-viewer-bot
https://github.com/jokmandis/Proxy-v1.3
https://github.com/jokmandis/upgrade-proxy
https://github.com/sayhellotothesky/TimeTravler
https://github.com/rsdh/Nexus-Roblox
https://github.com/nitin272/Adobe-After-Effects-Free-Download
https://github.com/DataAnalystSohrabAnsari/spotify-premium
https://github.com/cell012/Xbox-Game-Pass-Activator-Free-2024
https://github.com/brooklinyellow535/chatGPT-4-free-download-latest-updating
https://github.com/37185381/Adobe-Lightroom-Free
https://github.com/abrar-5888/Twitter-coinbot-2024
https://github.com/Atiq0629/seed-phrase-generator
https://github.com/Arisbatsi3/NitroDreams-2024
https://github.com/andjelaak6/IDA-Pro-Keygen-2024
https://github.com/Ahmeedkhaled/BrtWallet
https://github.com/ndyjan1337/fortnite-external
https://github.com/DVyadav2307/rust-hack-fr33
https://github.com/BanSamnang/rust-hack-fr33
https://github.com/Arisbatsi3/NitroDreams-2024
https://github.com/alexmoore00/Samourai-Wallet
https://github.com/buttercup28i69n/a-WorldofTanksa
https://github.com/mateito135798/sm64-emu
https://github.com/Rtyn1337/Thimble-bot-4.1
https://github.com/L3MO1337/Thimble-Exploit-Bot-4.0
https://github.com/Voq1210uBadIRaPeBY/68762t9wgsht1q
https://github.com/KyrilosNasr/Skinet4
https://github.com/chengxue2020/dszb
https://github.com/pakistani-tiktoker-imsha-rehman/.github
https://github.com/help-iq2/telethon
https://github.com/telethonArab/Arab
https://github.com/history26/ntt_hls
https://github.com/honeyman11/crypto-honeypot
https://github.com/honeyman11/solana-honeypot-smartcontract
https://github.com/hs622/newApp
https://github.com/jur1us/321
https://github.com/Katya1803/ITSS.20232.VuDinhVu.20215258
https://github.com/khederkasem/solrunner-solana-frontrun
https://github.com/khederkasem/solana-sniper-bot
https://github.com/oliverkarlsson1/SQUAD-SOFTWARE
https://github.com/openex-network/oex
https://github.com/rothqutra489/DOXCOIN-AUTOBOT
https://github.com/salwinat0r/Illegal_Product_Categorization
https://github.com/Santhiyaprakash/complaint_management_system
https://github.com/tqTitboy/hidden-wiki-2024
"""


SPECIAL_ACCOUNTS = {
    "GENERALGUIDECORPORATION": 139,  # Original repo count when reported
    "azkadev": 213  # Updated repo count
}


def parse_github_url(url: str) -> Tuple[str, str]:
    """Parse GitHub URL to extract owner and repo name."""
    # Remove trailing whitespace and newlines
    url = url.strip()
    # Extract owner/repo from URL like https://github.com/owner/repo
    match = re.match(r'https://github\.com/([^/]+)/([^/]+)/?$', url)
    if match:
        return match.group(1), match.group(2)
    return None, None


def get_reported_repositories() -> List[Tuple[str, str]]:
    """Extract repository owner/name pairs from the REPORTED_REPOS string."""
    repos = []
    for line in REPORTED_REPOS.strip().split('\n'):
        if line.strip():
            owner, repo = parse_github_url(line.strip())
            if owner and repo:
                repos.append((owner, repo))
    return repos


def check_repository_status(g: Github, owner: str, repo: str) -> Dict:
    """Check if a repository still exists and get its status."""
    try:
        repository = g.get_repo(f"{owner}/{repo}")
        return {
            'owner': owner,
            'repo': repo,
            'status': 'exists',
            'url': f"https://github.com/{owner}/{repo}",
            'created_at': repository.created_at,
            'updated_at': repository.updated_at,
            'stars': repository.stargazers_count,
            'forks': repository.forks_count,
            'archived': repository.archived,
            'disabled': repository.disabled,
            'private': repository.private
        }
    except GithubException as e:
        if e.status == 404:
            return {
                'owner': owner,
                'repo': repo,
                'status': 'not_found',
                'url': f"https://github.com/{owner}/{repo}",
                'error': 'Repository not found (removed or never existed)'
            }
        elif e.status == 403:
            return {
                'owner': owner,
                'repo': repo,
                'status': 'access_denied',
                'url': f"https://github.com/{owner}/{repo}",
                'error': 'Access denied (private or restricted)'
            }
        else:
            return {
                'owner': owner,
                'repo': repo,
                'status': 'error',
                'url': f"https://github.com/{owner}/{repo}",
                'error': f"Error {e.status}: {e.data.get('message', 'Unknown error')}"
            }
    except Exception as e:
        return {
            'owner': owner,
            'repo': repo,
            'status': 'error',
            'url': f"https://github.com/{owner}/{repo}",
            'error': str(e)
        }


def check_user_repository_count(g: Github, username: str) -> Dict:
    """Check how many public repositories a user currently has."""
    try:
        user = g.get_user(username)
        return {
            'username': username,
            'status': 'exists',
            'public_repos': user.public_repos,
            'total_private_repos': user.total_private_repos if hasattr(user, 'total_private_repos') else 'N/A',
            'created_at': user.created_at,
            'updated_at': user.updated_at,
            'url': f"https://github.com/{username}"
        }
    except GithubException as e:
        if e.status == 404:
            return {
                'username': username,
                'status': 'not_found',
                'url': f"https://github.com/{username}",
                'error': 'User not found (account removed or suspended)'
            }
        else:
            return {
                'username': username,
                'status': 'error',
                'url': f"https://github.com/{username}",
                'error': f"Error {e.status}: {e.data.get('message', 'Unknown error')}"
            }
    except Exception as e:
        return {
            'username': username,
            'status': 'error',
            'url': f"https://github.com/{username}",
            'error': str(e)
        }


def main():
    """Main function to check all reported repositories and special accounts."""
    logging.basicConfig(
        format="%(asctime)s (PID %(process)d) [%(levelname)s] %(filename)s:%(lineno)d %(message)s",
        level=logging.INFO,
        handlers=[logging.StreamHandler(sys.stdout)],
    )
    
    # Initialize GitHub API client using the same style as get_github_readmes.py
    g = Github(auth=Auth.Token(GITHUB_TOKENS[0]))
    logging.info("Using authenticated GitHub API with configured token")
    
    logging.info(f"Starting repository status check at {datetime.now()}")
    logging.info("=" * 80)
    
    # Get list of repositories to check
    repos_to_check = get_reported_repositories()
    logging.info(f"Found {len(repos_to_check)} repositories to check")
    
    # Check repository statuses
    results = []
    for i, (owner, repo) in enumerate(repos_to_check, 1):
        logging.info(f"Checking {i}/{len(repos_to_check)}: {owner}/{repo}")
        
        result = check_repository_status(g, owner, repo)
        results.append(result)
        
        status = result['status']
        if status == 'exists':
            logging.info(f"✅ {owner}/{repo} EXISTS (⭐{result['stars']}, 🍴{result['forks']})")
        elif status == 'not_found':
            logging.info(f"❌ {owner}/{repo} NOT FOUND")
        elif status == 'access_denied':
            logging.info(f"🔒 {owner}/{repo} ACCESS DENIED")
        else:
            logging.error(f"⚠️ {owner}/{repo} ERROR: {result['error']}")
        
        # Rate limiting - be nice to GitHub API
        time.sleep(0.5)
    
    logging.info("=" * 80)
    logging.info("REPOSITORY STATUS SUMMARY")
    logging.info("=" * 80)
    
    # Create summary statistics
    status_counts = {}
    for result in results:
        status = result['status']
        status_counts[status] = status_counts.get(status, 0) + 1
    
    total_repos = len(results)
    logging.info(f"Total repositories checked: {total_repos}")
    
    for status, count in status_counts.items():
        percentage = (count / total_repos) * 100
        logging.info(f"{status.upper()}: {count} ({percentage:.1f}%)")
    
    logging.info("=" * 80)
    logging.info("SPECIAL ACCOUNTS CHECK")
    logging.info("=" * 80)
    
    # Check special accounts where the entire account is a spam:
    # Also check how many repos are still there in the account as of now.
    # https://github.com/GENERALGUIDECORPORATION ((139 repositories))
    # https://github.com/azkadev ((213 repositories))
    for username, original_count in SPECIAL_ACCOUNTS.items():
        logging.info(f"Checking account: {username} (originally had {original_count} repos)")
        
        account_result = check_user_repository_count(g, username)
        
        if account_result['status'] == 'exists':
            current_count = account_result['public_repos']
            logging.info(f"  Status: ✅ Account exists")
            logging.info(f"  Current public repos: {current_count}")
            logging.info(f"  Original repo count: {original_count}")
            logging.info(f"  Change: {current_count - original_count:+d} repositories")
        elif account_result['status'] == 'not_found':
            logging.info(f"  Status: ❌ Account not found (suspended/removed)")
        else:
            logging.error(f"  Status: ⚠️ Error: {account_result['error']}")
    
    # Show some examples of existing repositories
    existing_results = [r for r in results if r['status'] == 'exists']
    if existing_results:
        logging.info("=" * 80)
        logging.info("REPOSITORIES THAT STILL EXIST")
        logging.info("=" * 80)
        logging.info(f"Found {len(existing_results)} repositories that still exist:")
        
        for i, repo in enumerate(existing_results[:10], 1):  # Show first 10
            archived_status = " (ARCHIVED)" if repo.get('archived') else ""
            disabled_status = " (DISABLED)" if repo.get('disabled') else ""
            logging.info(f"{i:2d}. {repo['owner']}/{repo['repo']} - ⭐{repo['stars']} 🍴{repo['forks']}{archived_status}{disabled_status}")
        
        if len(existing_results) > 10:
            logging.info(f"    ... and {len(existing_results) - 10} more repositories")
    else:
        logging.info("=" * 80)
        logging.info("NO REPOSITORIES STILL EXIST")
        logging.info("=" * 80)
    
    logging.info(f"Repository check completed at {datetime.now()}")


if __name__ == "__main__":
    main()
