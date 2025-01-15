import email
import os
import base64
from email.parser import BytesParser
from email.policy import default
from datetime import datetime

def get_email_display(email_str):
    # Extract name and email if in format "Name <email>"
    if '<' in email_str and '>' in email_str:
        name = email_str.split('<')[0].strip()
        email = email_str.split('<')[1].split('>')[0].strip()
        return name, email
    return email_str, email_str

def eml_to_html(eml_path, output_path):
    with open(eml_path, 'rb') as fp:
        eml_content = fp.read()
        eml_base64 = base64.b64encode(eml_content).decode()
        fp.seek(0)
        msg = BytesParser(policy=default).parse(fp)
    
    subject = msg.get('Subject', 'No Subject')
    from_addr_full = msg.get('From', 'No Sender')
    to_addr_full = msg.get('To', 'No Recipient')
    date = msg.get('Date', 'No Date')
    
    # Get proper name and email display
    from_name, from_email = get_email_display(from_addr_full)
    to_name, to_email = get_email_display(to_addr_full)
    
    # Extract HTML content if available, otherwise use plain text
    if msg.is_multipart():
        for part in msg.walk():
            if part.get_content_type() == "text/html":
                body = part.get_payload(decode=True).decode()
                break
            elif part.get_content_type() == "text/plain":
                body = part.get_payload(decode=True).decode()
                # Convert plain text to HTML
                body = body.replace('\n', '<br>')
                break
    else:
        body = msg.get_payload(decode=True).decode()
        if msg.get_content_type() == "text/plain":
            body = body.replace('\n', '<br>')

    html_content = f'''
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="UTF-8">
        <title>{subject}</title>
        <style>
            :root {{
                --bg-gradient-start: #8b5cf6;
                --bg-gradient-end: #d946ef;
                --text-primary: #1f2937;
                --text-secondary: #4b5563;
                --bg-white: #ffffff;
                --bg-gray-50: #f9fafb;
                --border-color: #e5e7eb;
            }}
            
            body {{
                margin: 0;
                padding: 40px 20px;
                min-height: 100vh;
                font-family: -apple-system, system-ui, BlinkMacSystemFont, 'Segoe UI', sans-serif;
                background: linear-gradient(135deg, var(--bg-gradient-start), var(--bg-gradient-end));
                color: var(--text-primary);
                line-height: 1.5;
                display: flex;
                justify-content: center;
            }}
            
            .container {{
                width: 100%;
                max-width: 800px;
                background: var(--bg-white);
                border-radius: 24px;
                overflow: hidden;
                box-shadow: 0 10px 25px rgba(0, 0, 0, 0.1);
            }}
            
            .header {{
                padding: 24px 32px;
                border-bottom: 1px solid var(--border-color);
                display: flex;
                justify-content: space-between;
                align-items: center;
            }}
            
            .title {{
                font-size: 24px;
                font-weight: 600;
                margin: 0;
            }}
            
            .download-btn {{
                background: #6366f1;
                color: white;
                border: none;
                padding: 12px 24px;
                border-radius: 12px;
                font-size: 14px;
                cursor: pointer;
                transition: all 0.2s;
            }}
            
            .download-btn:hover {{
                background: #4f46e5;
                transform: translateY(-1px);
            }}
            
            .sender-info {{
                padding: 24px 32px;
                background: var(--bg-gray-50);
                display: flex;
                align-items: center;
                gap: 16px;
            }}
            
            .avatar {{
                width: 48px;
                height: 48px;
                background: #e5e7eb;
                border-radius: 50%;
                display: flex;
                align-items: center;
                justify-content: center;
                font-weight: 500;
                color: var(--text-secondary);
            }}
            
            .sender-details {{
                flex: 1;
            }}
            
            .sender-name {{
                font-weight: 600;
                margin-bottom: 4px;
            }}
            
            .sender-title {{
                color: var(--text-secondary);
                font-size: 14px;
            }}
            
            .metadata {{
                padding: 24px 32px;
                border-bottom: 1px solid var(--border-color);
            }}
            
            .metadata-row {{
                display: grid;
                grid-template-columns: 80px 1fr;
                gap: 16px;
                margin-bottom: 8px;
            }}
            
            .metadata-label {{
                color: var(--text-secondary);
                font-weight: 500;
            }}
            
            .email-display {{
                display: flex;
                align-items: baseline;
                gap: 8px;
            }}
            
            .email-address {{
                color: var(--text-secondary);
                font-size: 0.9em;
            }}
            
            .email-content {{
                padding: 32px;
                background: white;
                line-height: 1.6;
            }}

            .info-alert {{
                position: fixed;
                top: 20px;
                right: 20px;
                background: white;
                padding: 16px 24px;
                border-radius: 12px;
                box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
                max-width: 300px;
                display: none;
                z-index: 1000;
            }}

            .email-content p {{
                margin: 0 0 16px 0;
            }}
        </style>
    </head>
    <body>
        <marquee>This email viewer which displays is an official email. The EML file contains the original email with complete metadata and digital signatures for verification.</marquee>

        <div class="info-alert" id="infoAlert">
            <strong>Verification Notice</strong>
            <p>This is an official email for university admission purposes. The EML file contains the original email with complete metadata and digital signatures for verification.</p>
        </div>

        <div class="container">
            <div class="header">
                <h1 class="title">{subject}</h1>
                <button class="download-btn" onclick="downloadEML()">
                    Download EML, the official email
                </button>
            </div>
            
            <div class="sender-info">
                <div class="avatar">
                    {from_name[0].upper()}
                </div>
                <div class="sender-details">
                    <div class="sender-name">{from_name}</div>
                    <div class="sender-title">{subject}</div>
                </div>
            </div>
            
            <div class="metadata">
                <div class="metadata-row">
                    <span class="metadata-label">From:</span>
                    <div class="email-display">
                        <span>{from_name}</span>
                        <span class="email-address">&lt;{from_email}&gt;</span>
                    </div>
                </div>
                <div class="metadata-row">
                    <span class="metadata-label">To:</span>
                    <div class="email-display">
                        <span>{to_name}</span>
                        <span class="email-address">&lt;{to_email}&gt;</span>
                    </div>
                </div>
                <div class="metadata-row">
                    <span class="metadata-label">Date:</span>
                    <span>{date}</span>
                </div>
            </div>
            
            <div class="email-content">
                {body}
            </div>
        </div>
        
        <script>
        document.addEventListener("DOMContentLoaded", function () {{
            const alert = document.getElementById('infoAlert');
            alert.style.display = 'block';
            setTimeout(() => {{
                alert.style.display = 'none';
            }}, 5000);
        }})

        function downloadEML() {{
            const emlContent = `{eml_base64}`;
            const blob = new Blob([Uint8Array.from(atob(emlContent), c => c.charCodeAt(0))], 
                {{ type: 'message/rfc822' }});
            const url = window.URL.createObjectURL(blob);
            const a = document.createElement('a');
            a.href = url;
            a.download = "{os.path.basename(eml_path)}";
            document.body.appendChild(a);
            a.click();
            window.URL.revokeObjectURL(url);
            document.body.removeChild(a);

            // Show info alert
        }}
        </script>
    </body>
    </html>
    '''
    
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(html_content)

# Main execution
if __name__ == "__main__":
    try:
        eml_to_html("paper.eml", "paper.html")
        print("Successfully converted TKS.eml to TKS.html")
    except Exception as e:
        print(f"An error occurred: {str(e)}")
