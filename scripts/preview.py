import re, sys, cairosvg
def preview(src, dst, width=1000, dark=True, strip=True):
    s = open(src).read()
    # resolve css vars: first :root block (dark default) or light block
    blocks = re.findall(r':root\{([^}]*)\}', s)
    vars_ = {}
    for b in (blocks[:1] if dark else blocks):
        for k, v in re.findall(r'(--[\w-]+):([^;]+)', b): vars_[k] = v.strip()
    s = re.sub(r'var\((--[\w-]+)\)', lambda m: vars_.get(m.group(1), '#f0f'), s)
    if strip: s = s.replace('opacity="0"', '')
    cairosvg.svg2png(bytestring=s.encode(), write_to=dst, output_width=width)
if __name__ == "__main__":
    preview(sys.argv[1], sys.argv[2], int(sys.argv[3]) if len(sys.argv) > 3 else 1000, (sys.argv[4] != 'light') if len(sys.argv) > 4 else True, 'scene' not in sys.argv[1])
