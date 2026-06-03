import html
import sys


def main():
    # 1. 引数がある場合は、引数の文字列を処理
    if len(sys.argv) > 1:
        raw_text = " ".join(sys.argv[1:])
        escaped_text = html.escape(raw_text)
        print(escaped_text)

    # 2. 引数がない場合は、標準入力を一括処理
    else:
        if sys.stdin.isatty():
            print(
                "Enter string to escape (Press Ctrl+D or Ctrl+Z to finish):",
                file=sys.stderr,
            )

        try:
            lines = []
            for line in sys.stdin:
                if "\x04" in line:
                    lines.append(line.replace("\x04", ""))
                    break
                lines.append(line)

            raw_text = "".join(lines)

            if raw_text:
                # 対話モードの場合のみ、入力と出力の境界を示す区切り線を標準エラー出力に表示
                if sys.stdin.isatty():
                    print("\n", "-" * 40, "\n", file=sys.stderr)

                print(
                    html.escape(raw_text), end="" if raw_text.endswith("\n") else "\n"
                )
        except (KeyboardInterrupt, EOFError):
            pass


if __name__ == "__main__":
    main()
