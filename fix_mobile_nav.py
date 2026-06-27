from pathlib import Path
import re

css_snippet = '''
    .mobile-nav{
      max-height: 0;
      opacity: 0;
      overflow: hidden;
      transition: max-height 0.35s ease, opacity 0.35s ease;
    }

    .mobile-nav.active{
      max-height: 480px;
      opacity: 1;
    }
'''

menu_html = '''
      <div class="mobile-nav md:hidden mt-4 rounded-3xl bg-[#081226]/95 px-5 py-5 text-white shadow-xl">
        <nav class="flex flex-col gap-4">
          <a href="index.html" class="block hover:text-blue-300 transition">Home</a>
          <a href="tours.html" class="block hover:text-blue-300 transition">Tours</a>
          <a href="about.html" class="block hover:text-blue-300 transition">About</a>
          <a href="services.html" class="block hover:text-blue-300 transition">Services</a>
          <a href="contact.html" class="block hover:text-blue-300 transition">Contact</a>
          <a href="contact.html" class="inline-flex justify-center bg-blue-600 hover:bg-blue-700 transition text-white px-6 py-3 rounded-full text-sm font-extrabold mt-3">Book Now</a>
        </nav>
      </div>
'''

script_snippet = '''
<script>
  document.addEventListener('DOMContentLoaded', function () {
    var menuButton = document.querySelector('.mobile-menu-button');
    var mobileNav = document.querySelector('.mobile-nav');
    if (!menuButton || !mobileNav) return;
    menuButton.addEventListener('click', function () {
      var isOpen = mobileNav.classList.toggle('active');
      menuButton.setAttribute('aria-expanded', isOpen);
    });
  });
</script>
'''

root = Path('.')
for file in sorted(root.glob('*.html')):
    text = file.read_text(encoding='utf-8')
    original = text

    # Update mobile button attributes and class
    text = text.replace(
        '<button class="md:hidden text-white">',
        '<button class="mobile-menu-button md:hidden text-white" aria-label="Toggle navigation" aria-expanded="false">'
    )

    # Insert mobile nav after the mobile button when present
    if 'class="mobile-nav md:hidden' not in text:
        mobile_button_pattern = r'(<!-- Mobile -->\s*<button[^>]*>\s*<i[^>]*>\s*</i>\s*</button>)'
        text, count = re.subn(mobile_button_pattern, r'\1\n' + menu_html, text, count=1)
        if count == 0:
            print(f'Warning: did not insert mobile menu into {file.name}')

    # Add CSS if missing
    if '.mobile-nav{' not in text:
        text = text.replace('</style>', css_snippet + '</style>', 1)

    # Add script if missing
    if 'querySelector(\'.mobile-menu-button\'' not in text:
        text = text.replace('</body>', script_snippet + '\n</body>', 1)

    if text != original:
        file.write_text(text, encoding='utf-8')
        print(f'Updated {file.name}')
