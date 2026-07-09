import os

import yaml


def build_tree(path, exclude_dirs):
    """
    指定されたパスのディレクトリ構造を辞書形式で再帰的に構築します。
    """
    d = {}
    try:
        for entry in os.scandir(path):
            # 除外対象のディレクトリ（.git や scripts など）はスキップ
            if entry.is_dir():
                if entry.name in exclude_dirs:
                    continue
                # ディレクトリの場合は再帰的に中身を取得
                d[entry.name] = build_tree(entry.path, exclude_dirs)
            elif entry.is_file():
                # ファイルの場合は値を None としてキーに追加
                d[entry.name] = None
    except PermissionError:
        # アクセス権限がないフォルダはスキップ
        pass
    return d


def main():
    # スクリプトの配置場所を基準に、プロジェクトのルートディレクトリを取得
    # scripts/tree.py から見て 1つ上の階層（..）
    base_dir = os.path.dirname(os.path.abspath(__file__))
    root_dir = os.path.abspath(os.path.join(base_dir, ".."))
    root_name = os.path.basename(root_dir)

    # 走査から除外するディレクトリのリスト
    exclude_dirs = {".git", "__pycache__", "node_modules", "venv", "node_modules", ".astro"}

    # ディレクトリ構造を辞書として構築
    tree_data = {root_name: build_tree(root_dir, exclude_dirs)}

    # YAML形式に変換して標準出力（ターミナル）に表示
    # sort_keys=False でファイル順序を維持します
    yaml_output = yaml.dump(tree_data, allow_unicode=True, sort_keys=False)
    print(yaml_output)


if __name__ == "__main__":
    main()
