aws是一個Amazon提供的雲端服務解決方案，我們主要使用他的運算資源進行模型訓練

絕大多數服務需**收費**且按時間或資源計費，請**使用完後隨手關閉或清空**，避免額外帳單

註冊帳號並登入 [here](aws.amazon.com)

# 控制台

登入後控制台如圖所示，紅圈部位為搜尋功能，直接使用搜尋搜尋想要的服務即可
可以在設定中進行帳單限額設置
注意右上角的區域選擇，預設應該是倫敦，這個涉及到實體機房問題，同一專案建議統一伺服器機房
![image](https://github.com/LassonLi/UOB_2024_LLM_EYE_HOSPTITAL/assets/63943203/fcd869f3-c407-4759-a30f-db632d1da239)

# EC2
EC2 服務是AWS提供的命令列形式雲端伺服器服務，需要圖形介面請啟動帶有 MATE的執行個體（但圖形介面很佔頻寬，容易造成不必要的消耗）

在控制台搜尋EC2並進入

點擊實例並點擊右上角啟動新實例來建立EC2服務
![image](https://github.com/LassonLi/UOB_2024_LLM_EYE_HOSPTITAL/assets/63943203/7c39ba38-adc5-4ad5-bae1-891549085629)

名稱隨意設置

藍筆勾出的分別為選擇系統類型和系統預裝服務，這裡因為是演示選擇免費類型，有deeplearning類型但是要收費

紅筆勾出的為具體伺服器配置，有許多不同種配置，具體參考[這裡](https://aws.amazon.com/cn/ec2/instance-types/)

模型訓練請參考特定需求，我們這裡選擇免費實例類型

![image](https://github.com/LassonLi/UOB_2024_LLM_EYE_HOSPTITAL/assets/63943203/11aea423-aa98-4f7a-b8e8-dde0c4b37346)

接著點擊創建新密鑰對，保存好你的私鑰

![image](https://github.com/LassonLi/UOB_2024_LLM_EYE_HOSPTITAL/assets/63943203/0e4eabc6-dd98-4ca0-acd7-96b5232445e1)

點選網路設定上的編輯，新加入一條安全群組規則

將連接埠8080-8089開放，不然只能透過ssh連結伺服器，不能透過網頁存取
![image](https://github.com/LassonLi/UOB_2024_LLM_EYE_HOSPTITAL/assets/63943203/c741f188-3dda-4580-a892-3d89383cb027)

然後設定儲存大小，然後點擊啟動實例即可。

## 連接到EC2
回到實例介面，應該會看到你剛剛新建的實例，點選連線即可進入伺服器，記得設定使用者名，預設也行
![image](https://github.com/LassonLi/UOB_2024_LLM_EYE_HOSPTITAL/assets/63943203/cf91210a-053d-490c-9c23-e7c04c39f065)

接下來就是熟悉的linux介面啦

Amazon linux的套件管理器和部分指令有些許不同，但是推薦用它

這東西叫yum，具體自己搜尋教學

因為是可以內部網路下載包，比較省流量
但我們主要不使用ec2，因為他開機就要錢，太貴了
![image](https://github.com/LassonLi/UOB_2024_LLM_EYE_HOSPTITAL/assets/63943203/00ebfd6d-e0f9-4abf-9a2c-740ca1260ca7)

# sagemaker
sagemaker 是Amazon開放的一款專門用於機器學習的解決方案，完整到從資料標註到資料分析都有

但太貴了，我們只用模型訓練的部分，其餘部分有興趣自己學習

回到控制台，搜尋sagemaker， 進入notebook
![image](https://github.com/LassonLi/UOB_2024_LLM_EYE_HOSPTITAL/assets/63943203/3fae4e67-4c08-4870-a7c2-d6bf03a8397a)
點選建立筆記本實例

這裡的筆記本實例類型並非我們模型運行時使用的伺服器配置

而是運行jupyter時的伺服器，因此選個盡量低配和能運行資料載入預處理的就行

下方的配置git，看狀況配置
![image](https://github.com/LassonLi/UOB_2024_LLM_EYE_HOSPTITAL/assets/63943203/01cb9e64-6f75-4091-8c29-2cc6​​d03ad662)

然後回到主介面點選對應的筆記本 啟動jupyter，我們就來到了熟悉的jupyter

點選新建命令列，由於這是aws的jupyter，指令不會在電腦的terminal裡面輸出，因此會在這個新建的terminal裡面輸出

最右邊有sagemaker的機器學習example，建議至少看一個

![image](https://github.com/LassonLi/UOB_2024_LLM_EYE_HOSPTITAL/assets/63943203/2994ead8-9f0e-44a7-9824-465a45e03393)

這裡涉及到一個將資料從s3儲存桶中載入的過程，我們也可以使用s3儲存筒，來避免重複上傳資料造成的頻寬浪費（主要是費錢）
![image](https://github.com/LassonLi/UOB_2024_LLM_EYE_HOSPTITAL/assets/63943203/519c1e0b-0876-4ad5-851e-36511fe19760)

##訓練模型
具體來說，sagemaker有一個sagemaker套件來訓練模型和呼叫aws伺服器資源

這裡是使用sagemaker套件定義伺服器類型，這才是真正訓練模型的伺服器，同時，一旦摁下程式運行按鈕，這個伺服器就會**開始計費**

後續有如何用sagemaker套件建立訓練任務的程式碼，請自行閱讀任一example
![image](https://github.com/LassonLi/UOB_2024_LLM_EYE_HOSPTITAL/assets/63943203/f44c64b8-f933-4876-bfcf-e9703b4431db)

# S3
S3儲存筒，就是一個雲端儲存系統，控制台搜S3

直接新建一個上傳資料就行，注意別重複上傳，他是隨用隨付錢的，反正要錢，如有需要，用它
