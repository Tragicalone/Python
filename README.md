# Python
最後編輯日 2018/11/26

# Git
git config --global user.name            <--- 查詢 Git Hub 帳號
git config --global user.email           <--- 查詢 Git Hub 帳號 Email
git clone https://github.com/Tragicalone <--- 複製 Tragicalone 的 Git Hub 到目前資料夾
git add 檔案名                           <--- 將檔案加入 Git 追蹤
git commit -m "訊息"                     <--- 同意檔案的變更並加註訊息 
git push                                 <--- 將同意的變更上傳至 Git Hub
git diff
git log --oneline --graph
git reflog
git reset --hard HEAD^^
git reset --hard TheNumber
git checkout TheBranch
git merge --no-ff -m "Accept message" TheBranch
git remote -v

#Jupyter
pip install "ipython[notebook]"   <--- 安裝 Jupyter
ipython notebook                  <--- 於目前目錄啟動 Jupyter Service
