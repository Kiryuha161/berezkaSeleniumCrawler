def get_headers(access_token):
    headers = {
        "accept": "application/json, text/plain, */*",
        "accept-encoding": "gzip, deflate, br, zstd",
        "accept-language": "ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7",
        "authorization": f"Bearer {access_token}",
        "cache-control": "no-cache",
        "content-type": "application/json; charset=UTF-8",
        "origin": "https://agregatoreat.ru",
        "pragma": "no-cache",
        "referer": "https://agregatoreat.ru/",
        "sec-ch-ua": '"Chromium";v="130", "Google Chrome";v="130", "Not?A_Brand";v="99"',
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": '"Windows"',
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-site",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36"
    }

    return headers

    #eyJhbGciOiJSUzI1NiIsImtpZCI6IjBDOTgyMzhGNEE3OUU3RjExN0U5OUJGMTQ4N0M5ODA0IiwidHlwIjoiYXQrand0In0.eyJpc3MiOiJodHRwczovL2xvZ2luLmFncmVnYXRvcmVhdC5ydSIsIm5iZiI6MTczMTY3NjE1MywiaWF0IjoxNzMxNjc2MTUzLCJleHAiOjE3MzE2Nzk3NTMsImF1ZCI6InVpLWFwaSIsInNjb3BlIjpbIm9wZW5pZCIsInByb2ZpbGUiLCJ1aS1hcGkiXSwiYW1yIjpbInB3ZCJdLCJjbGllbnRfaWQiOiJlYXRfdWkiLCJzdWIiOiI5MmZiOWVkOC02NzYzLTQ3ODgtYWQ0NC1hMDI4NDczNmYzMWYiLCJhdXRoX3RpbWUiOjE3MzE2NzIyODUsImlkcCI6ImxvY2FsIiwib3JnYW5pemF0aW9uX2lkIjoiNjg1ODk2MzYtOGJkNS00NTg2LWFmOWYtODZlZTdlMDcwNjBiIiwiY2xpZW50X3R5cGUiOiJTdXBwbGllciIsInNpZCI6IjkwRTE4MkNCQ0VEMDM4ODlGNUI3RkVEMEI1OEMyM0RDIiwianRpIjoiNUY2NTBGREMzOEFBOTMyQTBENzk2MzA0REQ2RTU1NTUifQ.WfcFTNUvZBow2sfLgnQWjEMmOxGEJWHJQGKgAioG0NW9HJophk - XSkfsJAsEr2Ae5NiTeLQRETmCLXRezaPglKranFIwURXhGYMEqheONKxlrqkQBXsIoi - pZgojaYgg2SFmHdNU6BN0DZJcjKzVE8CF6xz8tj2CVdsvn2jG8ZnAmNFdIa8TjRdIXvrY51_ViDu0HWzGW76aQ9nFtRbZOGgOuQty1zuAE7Kosxpn1pzBTDXuuacuZzX6TVqoMzHitsnXjmRcne2DD2wWXnbbldR60sZ67jCTGcye0dfSMF3Cvy50XooWrW0JR3DXWsyLREnVO_amtEqV9Oy0Dkjb3A
