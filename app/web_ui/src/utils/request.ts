import axios from 'axios'
const client = axios.create({
  baseURL: 'http://localhost:8757',
  timeout: 5000,
})

async function stream_client(url: string, options: RequestInit = {}) {
  const response = await fetch(`http://localhost:8757${url}`, {
    ...options,
    headers: {
      'Content-Type': 'application/json',
      ...(options.headers || {}),
    },
  })

  if (!response.ok || !response.body) {
    throw new Error(`HTTP error! Status: ${response.status}`)
  }

  const reader = response.body.getReader()
  const decoder = new TextDecoder('utf-8')

  return new ReadableStream({
    async start(controller) {
      while (true) {
        const { done, value } = await reader.read()
        if (done) {
          controller.close()
          break
        }
        controller.enqueue(decoder.decode(value, { stream: true }))
      }
    },
  })
}

export default { client, stream_client }
