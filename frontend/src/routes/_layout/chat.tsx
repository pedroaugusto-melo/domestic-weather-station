import { createFileRoute } from "@tanstack/react-router"
import { ChatInterface } from "../../components/Chatbot/ChatInterface"

export const Route = createFileRoute("/_layout/chat")({
  component: ChatPage,
})

function ChatPage() {
  return <ChatInterface />
} 