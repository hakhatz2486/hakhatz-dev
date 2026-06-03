import html
import sys


def main():
    # 1. 引数がある場合は、引数の文字列を処理
    if len(sys.argv) > 1:
        # 複数の引数がある場合はスペースで結合
        raw_text = " ".join(sys.argv[1:])
        escaped_text = html.escape(raw_text)
        print(escaped_text)

    # 2. 引数がない場合は、標準入力を待機（パイプ受付など）
    else:
        # ターミナルが対話モードの場合は、ユーザーに入力を促す
        if sys.stdin.isatty():
            try:
                raw_text = input("Enter string to escape: ")
                print(html.escape(raw_text))
            except (KeyboardInterrupt, EOFError):
                pass
        else:
            # パイプやリダイレクト経由での入力を一括処理
            raw_text = sys.stdin.read()
            # 末尾の余分な改行コードを除去したい場合は .rstrip('\n') を追加してください
            print(html.escape(raw_text), end="")


if __name__ == "__main__":
    main()
