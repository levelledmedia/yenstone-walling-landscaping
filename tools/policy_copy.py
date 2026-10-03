"""
Copy for the privacy policy page (site/privacy-policy.html), used by build-pages.py.

CONFIRM with client: this is a plain, general-purpose policy written only from what the site does today
(enquiry form, phone and email, Google Fonts, an OpenStreetMap map, no analytics and no cookies).
Update it if the client adds analytics, a form service, newsletters, a booking system or anything else
that handles personal data, and have it reviewed before launch.
"""

INTRO = ('This policy explains what personal information Yenstone Walling &amp; Landscaping Ltd collects through this website '
         'and when you get in touch, how we use it, and the choices you have.')

# (heading, html body)
SECTIONS = [
    ('Who we are', '''
            <p>This website is run by Yenstone Walling &amp; Landscaping Ltd. We are the controller of the personal information described in this policy, which means we decide how and why it is used.</p>
            <p>Perhams Farm, Sally Lovells Lane, Yenston, Templecombe, Somerset BA8 0NE<br>
            Phone: <a href="tel:01963371123">01963 371123</a><br>
            Email: <a href="mailto:info@yenstonewalling.co.uk">info@yenstonewalling.co.uk</a></p>'''),

    ('What information we collect', '''
            <p>We collect the information you choose to give us when you contact us by phone, email or the form on this website, or when we visit and quote for a job. This may include:</p>
            <ul>
              <li>your name</li>
              <li>your phone number and email address</li>
              <li>the address or location of the property</li>
              <li>details of the work you are asking about, and any photos you send us</li>
            </ul>
            <p>Like most websites, our web hosting may also record basic technical information when you visit, such as your IP address, browser type and the pages you view.</p>'''),

    ('How we use it', '''
            <p>We use your information to:</p>
            <ul>
              <li>reply to your enquiry and arrange a visit</li>
              <li>prepare quotes, and carry out and manage the work</li>
              <li>keep records of our work and our business, including accounts</li>
              <li>keep this website secure and working properly</li>
              <li>meet our legal obligations</li>
            </ul>
            <p>We do not use your information for automated decision-making.</p>'''),

    ('Our legal basis', '''
            <p>Under data protection law we need a legal basis to use your information. Ours are:</p>
            <ul>
              <li>to take steps at your request before a contract, and to carry out a contract with you</li>
              <li>our legitimate interests in answering enquiries and running our business, where these are not outweighed by your rights</li>
              <li>meeting legal obligations, such as keeping financial records</li>
            </ul>'''),

    ('Who we share it with', '''
            <p>We do not sell your personal information. We only share it with people who help us run the business, such as website hosting and email providers, accountants and professional advisers, or where we are required to by law. We ask them to keep it secure and to use it only for the purpose we gave it to them.</p>'''),

    ('Third-party content on this website', '''
            <p>To work as it does, this website loads some content from other providers. When it does, they may receive your IP address and basic details about your device:</p>
            <ul>
              <li>fonts from Google Fonts (<a href="https://policies.google.com/privacy" target="_blank" rel="noopener">Google privacy policy</a>)</li>
              <li>the map on our pages from OpenStreetMap (<a href="https://wiki.osmfoundation.org/wiki/Privacy_Policy" target="_blank" rel="noopener">OpenStreetMap privacy policy</a>)</li>
            </ul>
            <p>These providers have their own privacy policies, and we do not control how they use this information.</p>'''),

    ('Cookies', '''
            <p>We do not use cookies on this website to track you or for advertising. If that changes, we will update this policy and ask for your consent where the law requires it.</p>'''),

    ('How long we keep it', '''
            <p>We keep your information only for as long as we need it for the reasons above. For example, enquiries that do not lead to work are not kept for long, while records of completed work and accounts are kept for as long as the law requires. After that we delete or anonymise them.</p>'''),

    ('Keeping it secure', '''
            <p>We take reasonable steps to protect your information. No method of sending information over the internet or storing it electronically is completely secure, so we cannot guarantee absolute security.</p>'''),

    ('Your rights', '''
            <p>You have the right to:</p>
            <ul>
              <li>ask for a copy of the personal information we hold about you</li>
              <li>ask us to correct anything that is wrong or incomplete</li>
              <li>ask us to delete your information, or to restrict how we use it</li>
              <li>object to us using your information where we rely on our legitimate interests</li>
            </ul>
            <p>To use any of these rights, contact us using the details above. If you are unhappy with how we have handled your information, you can complain to the Information Commissioner's Office at <a href="https://ico.org.uk" target="_blank" rel="noopener">ico.org.uk</a> or on 0303 123 1113. We would appreciate the chance to put things right first.</p>'''),

    ('Changes to this policy', '''
            <p>We may update this policy from time to time. The latest version will always be on this page.</p>
            <p>Last updated: October 2026.</p>'''),
]
