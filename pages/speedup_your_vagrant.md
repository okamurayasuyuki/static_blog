title: Vagrantの性能が遅さをnfsで解決
date: 2013-09-03
tags: vagrant,ubuntu

最近はVagrantにつないでその中で開発を行っているけど、shared_folderの反応がすごい遅いし、
git コマンドもインデックスに登録されたフォルダー数が多いとレスポンスがめちゃくちゃ遅い。

これは仮想環境で開発ができないのでは、、と思っていたけどnfsで解決できた。

    config.vm.synced_folder ".","/vagrant", :nfs => true

こんなかんじに書くと早くなる。ぜんぜん違う。
これで仮想環境でちゃんとプログラミングできる。

