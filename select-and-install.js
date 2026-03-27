const { exec } = require('child_process')
const inquirer = require('inquirer')

// 用 Copilot CLI 列出所有 plugin
function getPlugins(callback) {
  exec('copilot plugin list', (err, stdout, stderr) => {
    if (err) {
      console.error('Failed to run "copilot plugin list":', stderr || err.message)
      callback([])
      return
    }

    const plugins = stdout
      .split('\n')
      .map(line => line.trim())
      .filter(line => line)
      .map(line => line.split(' ')[0]) // 取出 plugin name，預設值是第一個欄位

    callback(plugins)
  })
}

// 用 inquirer 啟動互動勾選（預設全選）
inquirer
  .prompt([
    {
      type: 'checkbox',
      name: 'selected',
      message: '選擇要安裝的 plugin（預設全部已勾選，按空格取消不想要的）',
      choices: function () {
        return new Promise(resolve => {
          getPlugins(plugins => {
            // 陣列元素：{ name, value, checked: true }
            const choices = plugins.map(p => ({
              name: p,
              value: p,
              checked: true
            }))
            resolve(choices)
          })
        })
      }
    }
  ])
  .then(answers => {
    if (!answers.selected || answers.selected.length === 0) {
      console.log('未選擇任何 plugin，退出。')
      return
    }

    console.log(`開始安裝 ${answers.selected.length} 個 plugin：`)
    answers.selected.forEach(plugin => {
      console.log(`> 安裝 plugin: ${plugin}`)
      exec(`copilot plugin install ${plugin}`, (err, stdout, stderr) => {
        if (err) {
          console.error(`✗ 安裝失敗 ${plugin}：`, stderr || err.message)
          return
        }
        console.log(`✓ 安裝完成 ${plugin}\n${stdout}`)
      })
    })
  })
  .catch(err => {
    console.error('選單執行錯誤：', err)
  })
