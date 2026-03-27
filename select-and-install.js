#!/usr/bin/env node
const { exec } = require('child_process')
const fs = require('fs')
const path = require('path')
const inquirer = require('inquirer')

const pluginsDir = path.join(__dirname, 'plugins')

// 讀取本地 plugins/ 目錄，取得所有可安裝的 plugin
function getPlugins() {
  try {
    return fs.readdirSync(pluginsDir)
      .filter(name => fs.statSync(path.join(pluginsDir, name)).isDirectory())
      .map(name => {
        const pluginJsonPath = path.join(pluginsDir, name, 'plugin.json')
        let description = ''
        try {
          const meta = JSON.parse(fs.readFileSync(pluginJsonPath, 'utf8'))
          if (meta.description) description = ` - ${meta.description}`
        } catch {}
        return {
          name: `${name}${description}`,
          value: name,
          checked: true
        }
      })
  } catch (err) {
    console.error('無法讀取 plugins 目錄：', err.message)
    return []
  }
}

const choices = getPlugins()

if (choices.length === 0) {
  console.log('找不到任何可安裝的 plugin，退出。')
  process.exit(1)
}

// 用 inquirer 啟動互動勾選（預設全選，按空格取消）
inquirer
  .prompt([
    {
      type: 'checkbox',
      name: 'selected',
      message: '選擇要安裝的 plugin（預設全部已勾選，按空格取消不想要的）：',
      choices
    }
  ])
  .then(answers => {
    if (!answers.selected || answers.selected.length === 0) {
      console.log('未選擇任何 plugin，退出。')
      return
    }

    console.log(`\n開始安裝 ${answers.selected.length} 個 plugin：`)
    answers.selected.forEach(plugin => {
      const pluginPath = path.join(pluginsDir, plugin)
      console.log(`> 安裝 plugin: ${plugin}`)
      exec(`copilot skill install "${pluginPath}"`, (err, stdout, stderr) => {
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
