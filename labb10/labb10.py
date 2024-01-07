import re

def checkEmail():
    mtxt = "jox r.nohre@jth.hj.se, bjox@se, adam@example.com, jox@jox@jox.com."
    test = re.findall(r"(?:^|\s)([\w.]+?@[\w]+\.[\w\.]+[\w])", mtxt)
    print(test)

def simpson():
    with open("labb10/tabla.html", "r", encoding="utf-8") as f:
        txt = f.read()

    regex_pattern = (
        r"<td class=\"svtTablaTime\">\s+"
        r"(\d+\.\d+)\s+"
        r"</td>\s+"
        r"<td class=\"svtJsTablaShowInfo\">\s+"
        r"<h4 class=\"svtLink-hover svtTablaHeading\">\s+"
        r"Simpsons\s+"
        r"</h4>\s+"
        r"<div class=\"svtJsStopPropagation\">\s+"
        r"<div class=\"svtTablaTitleInfo svtHide-Js\">\s+"
        r"<div class=\"svtTablaContent-Description\">\s+"
        r"<p class=\"svtXMargin-Bottom-10px\">\s+Amerikansk animerad komediserie från [\d-]+\. Säsong (\d+)\. Del (\d+) av (\d+)\.(.+?)\s+"
        r"</p>"
    )

    collect_information = re.findall(regex_pattern, txt)

    for x in collect_information:
        time = x[0]
        season = x[1]
        episode = f"{x[2]}\\{x[3]}"
        description = x[4]
        print("-" * 50)
        print(f"time: {time}\nseason: {season}\nepisode: {episode}\ndescription: {description}\n")

checkEmail()
simpson()