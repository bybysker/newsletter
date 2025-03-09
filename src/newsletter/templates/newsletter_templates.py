"""
Newsletter HTML templates.
This file contains all the HTML template strings used in newsletter generation.
"""

# HTML head with styles
HTML_HEAD = """
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Newsletter</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            line-height: 1.6;
            margin: 0;
            padding: 20px;
            color: #333;
        }
        .newsletter-container {
            max-width: 800px;
            margin: 0 auto;
            padding: 20px;
            background-color: #fff;
            box-shadow: 0 0 10px rgba(0,0,0,0.1);
        }
        .abstract {
            background-color: #f9f9f9;
            padding: 15px;
            margin-bottom: 20px;
            border-left: 4px solid #0066cc;
        }
        .summary {
            margin-bottom: 30px;
            padding-bottom: 20px;
            border-bottom: 1px solid #eee;
        }
        .summary-title {
            color: #0066cc;
            font-size: 18px;
            margin-bottom: 10px;
        }
        .summary-image {
            max-width: 100%;
            height: auto;
            background-color: #f0f0f0;
            display: block;
            margin: 10px 0;
            text-align: center;
            padding: 30px 0;
            color: #666;
        }
        .summary-content {
            margin-bottom: 10px;
        }
        .source {
            font-style: italic;
            font-size: 14px;
            color: #666;
        }
        .other-news {
            background-color: #f9f9f9;
            padding: 15px;
            margin-top: 20px;
        }
        .other-news h2 {
            font-size: 18px;
            color: #333;
            margin-bottom: 10px;
        }
        .other-news-links {
            list-style-type: none;
            padding-left: 0;
        }
        .other-news-links li {
            margin-bottom: 5px;
        }
        a {
            color: #0066cc;
            text-decoration: none;
        }
        a:hover {
            text-decoration: underline;
        }
    </style>
</head>
<body>
    <div class="newsletter-container">
"""

# Abstract section template
ABSTRACT_SECTION = """
        <div class="abstract">
            <h1>Newsletter</h1>
            <p>{abstract}</p>
        </div>
"""

# Summary section template for each summary
SUMMARY_SECTION = """
        <div class="summary">
            <h2 class="summary-title">{title}</h2>
            <div class="summary-image">[Image Placeholder]</div>
            <div class="summary-content">
                <p>{content}</p>
            </div>
            <div class="source">Source: <a href="{link}" target="_blank">{link}</a></div>
        </div>
"""

# Other news section start template
OTHER_NEWS_START = """
        <div class="other-news">
            <h2>Other News:</h2>
            <ul class="other-news-links">
"""

# Other news link item template
OTHER_NEWS_LINK = """
                <li><a href="{link}" target="_blank">{link}</a></li>
"""

# Other news section end template
OTHER_NEWS_END = """
            </ul>
        </div>
"""

# HTML footer template
HTML_FOOTER = """
    </div>
</body>
</html>
""" 