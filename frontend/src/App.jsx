import React, { useEffect, useState } from 'react'

const API_BASE = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000'

export default function App(){
  const [todos, setTodos] = useState([])
  const [text, setText] = useState('')
  const [status, setStatus] = useState('')

  // direct add inputs
  const [titleInput, setTitleInput] = useState('')
  const [dueInput, setDueInput] = useState('')

  // edit state
  const [editId, setEditId] = useState(null)
  const [editTitle, setEditTitle] = useState('')
  const [editDue, setEditDue] = useState('')

  useEffect(()=>{ fetchTodos() }, [])

  async function fetchTodos(){
    try{
      const res = await fetch(`${API_BASE}/todos`)
      const data = await res.json()
      setTodos(data)
    }catch(e){
      setStatus('Todos の取得に失敗しました')
    }
  }

  async function submit(){
    if(!text) return
    setStatus('送信中...')
    try{
      const res = await fetch(`${API_BASE}/input?text=${encodeURIComponent(text)}`, { method: 'POST' })
      const data = await res.json()
      setStatus(JSON.stringify(data))
      setText('')
      await fetchTodos()
    }catch(e){
      setStatus('送信に失敗しました')
    }
  }

  async function addDirect(){
    if(!titleInput) return
    setStatus('追加中...')
    try{
      const res = await fetch(`${API_BASE}/todos`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ title: titleInput, due_date: dueInput || null })
      })
      const data = await res.json()
      setStatus(JSON.stringify(data))
      setTitleInput('')
      setDueInput('')
      await fetchTodos()
    }catch(e){
      setStatus('追加に失敗しました')
    }
  }

  async function markComplete(todo){
    // 直接完了APIを呼び出す（LLM を経由しない確実な方法）
    setStatus('完了中...')
    try{
      const res = await fetch(`${API_BASE}/todos/${todo.id}/complete`, { method: 'POST' })
      const data = await res.json()
      setStatus(JSON.stringify(data))
      await fetchTodos()
    }catch(e){
      setStatus('処理に失敗しました')
    }
  }

  function startEdit(todo){
    setEditId(todo.id)
    setEditTitle(todo.title || '')
    setEditDue(todo.due_date || '')
  }

  function cancelEdit(){
    setEditId(null)
    setEditTitle('')
    setEditDue('')
  }

  async function saveEdit(id){
    if(!editTitle) return setStatus('タイトルを入力してください')
    setStatus('保存中...')
    try{
      const res = await fetch(`${API_BASE}/todos/${id}`, {
        method: 'PUT',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ title: editTitle, due_date: editDue || null })
      })
      const data = await res.json()
      setStatus(JSON.stringify(data))
      cancelEdit()
      await fetchTodos()
    }catch(e){
      setStatus('保存に失敗しました')
    }
  }

  return (
    <div className="container">
      <h1>LLM構造化Todoデモ</h1>

      <section className="section direct-add">
        <div style={{display:'flex',flexDirection:'column',gap:8}}>
          <h2 style={{marginBottom:6}}>直接追加 </h2>
          <div style={{display:'flex',gap:8}}>
            <input value={titleInput} onChange={e=>setTitleInput(e.target.value)} placeholder="タスクタイトル" />
            <input value={dueInput} onChange={e=>setDueInput(e.target.value)} placeholder="期限 (YYYY-MM-DD 任意)" />
            <button className="btn btn-ghost" onClick={addDirect}>追加</button>
          </div>
        </div>
      </section>

      <section className="section input">
        <h2>自然言語で追加</h2>
        <textarea value={text} onChange={e=>setText(e.target.value)} placeholder="例: 明日までにレポートを作成するタスクを追加してください"></textarea>
        <div className="actions">
          <button className="btn" onClick={submit}>送信</button>
        </div>
        <div className="status">{status}</div>
      </section>


      <section className="section list">
        <div className="list-card">
          <div className="list-header">
            <h2>
              Todo 一覧
              <button className="refresh" onClick={fetchTodos} aria-label="一覧を更新">
                <span className="icon" aria-hidden></span>
                <span className="label">一覧を更新</span>
              </button>
            </h2>
          </div>

          <ul>
            {todos.length === 0 && <li style={{padding:16}}>タスクはありません</li>}
            {todos.map(todo => (
              <li key={todo.id} className={todo.completed ? 'completed' : ''}>
                {editId === todo.id ? (
                  <div style={{display:'flex',flexDirection:'column',gap:8}}>
                    <input value={editTitle} onChange={e=>setEditTitle(e.target.value)} />
                    <div style={{display:'flex',gap:8,alignItems:'center'}}>
                      <input value={editDue} onChange={e=>setEditDue(e.target.value)} placeholder="期限 (YYYY-MM-DD 任意)" />
                      <button className="btn" onClick={()=>saveEdit(todo.id)}>保存</button>
                      <button className="btn btn-ghost" onClick={cancelEdit}>キャンセル</button>
                    </div>
                  </div>
                ) : (
                  <>
                    <div className="row">
                      <div className="title">{todo.title} {todo.due_date && <span className="due">({todo.due_date})</span>}</div>
                      <div className="meta">
                        <span className="meta-id">#{todo.id}</span>
                        <span className={`meta-status ${todo.completed ? 'done' : 'pending'}`}>{todo.completed ? '完了' : '未完了'}</span>
                      </div>
                      <div className="actions-inline">
                        {!todo.completed && (
                          <button className="btn-icon" onClick={()=>markComplete(todo)} aria-label={`完了: ${todo.title}`} title="完了">
                            <span className="icon">✔︎</span>
                          </button>
                        )}
                        <button className="btn btn-ghost btn-small" onClick={()=>startEdit(todo)} style={{marginLeft:8}}>編集</button>
                      </div>
                    </div>
                  </>
                )}
              </li>
            ))}
          </ul>
        </div>
      </section>

      <footer>API: <code>{API_BASE}</code></footer>
    </div>
  )
}
