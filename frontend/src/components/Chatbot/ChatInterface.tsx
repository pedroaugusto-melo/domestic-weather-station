import {
  Box,
  VStack,
  Input,
  Button,
  Text,
  Flex,
  useColorModeValue,
  Container,
  InputGroup,
  InputRightElement,
  keyframes,
  Avatar,
  Heading,
  Icon,
  SimpleGrid,
  Spinner,
} from "@chakra-ui/react"
import { useState, useRef, useEffect } from "react"
import { useSensorData } from "../../hooks/useSensorData"
import { useChat } from "../../hooks/useChat"
import { FiSend, FiThermometer, FiDroplet, FiAlertTriangle } from "react-icons/fi"
import { FaRobot } from "react-icons/fa"
import { FaUserCircle } from "react-icons/fa"
import { StatCard } from "../Common/StatCard"

interface Message {
  role: "user" | "assistant"
  content: string
  isLoading?: boolean
}

// Create a loading dots animation
const loadingDots = keyframes`
  0% { content: "."; }
  33% { content: ".."; }
  66% { content: "..."; }
  100% { content: "."; }
`

export function ChatInterface() {
  const [messages, setMessages] = useState<Message[]>([])
  const [input, setInput] = useState("")
  const messagesEndRef = useRef<HTMLDivElement>(null)
  const { data: sensorData, isLoading: isSensorDataLoading, error: sensorError } = useSensorData(5000)
  const { sendMessage, isLoading: isChatLoading } = useChat()
  
  const bgColor = useColorModeValue("gray.50", "gray.700")
  const messageBgUser = useColorModeValue("blue.100", "blue.700")
  const messageBgAssistant = useColorModeValue("gray.100", "gray.600")
  const borderColor = useColorModeValue("gray.200", "gray.600")

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" })
  }

  useEffect(() => {
    scrollToBottom()
  }, [messages])

  const handleSend = async () => {
    if (!input.trim() || !sensorData) return

    const userMessage: Message = {
      role: "user",
      content: input,
    }

    setMessages(prev => [...prev, userMessage])
    setInput("")

    // Add loading message
    const loadingMessage: Message = {
      role: "assistant",
      content: "",
      isLoading: true
    }
    setMessages(prev => [...prev, loadingMessage])

    try {
      const response = await sendMessage(input, {
        temperature: Number(sensorData.temperature.current?.value ?? 0),
        humidity: Number(sensorData.humidity.current?.value ?? 0),
        toxicGases: Number(sensorData.toxicGases.current?.value ?? 0),
      })
      // Remove loading message and add actual response
      setMessages(prev => {
        const withoutLoading = prev.filter(msg => !msg.isLoading)
        return [...withoutLoading, {
          role: "assistant",
          content: response,
        }]
      })
    } catch (error) {
      // Remove loading message on error
      setMessages(prev => prev.filter(msg => !msg.isLoading))
      console.error("Error sending message:", error)
    }
  }

  if (isSensorDataLoading) {
    return (
      <Container maxW="container.lg" py={8}>
        <VStack spacing={4} h="80vh">
          <Heading size="lg" alignSelf="flex-start" mb={4}>
            Assistente Virtual
          </Heading>
          <Flex justify="center" align="center" h="100%">
            <Spinner size="xl" />
          </Flex>
        </VStack>
      </Container>
    )
  }

  if (sensorError) {
    return (
      <Container maxW="container.lg" py={8}>
        <VStack spacing={4} h="80vh">
          <Heading size="lg" alignSelf="flex-start" mb={4}>
            Assistente Virtual
          </Heading>
          <Flex justify="center" align="center" h="100%" color="red.500">
            <Text>Error loading sensor data. Please try again later.</Text>
          </Flex>
        </VStack>
      </Container>
    )
  }

  return (
    <Container maxW="container.lg" py={8}>
      <VStack spacing={4} h="80vh">
        <Heading size="lg" alignSelf="flex-start" mb={4}>
          Assistente Virtual
        </Heading>

        <SimpleGrid columns={{ base: 1, md: 3 }} spacing={6} w="100%" mb={4}>
          <StatCard
            title="Temperatura Atual"
            value={`${sensorData?.temperature.current?.value || 0}°C`}
            icon={FiThermometer}
            helpText={`Última atualização: ${new Date(sensorData?.temperature.current?.read_at || '').toLocaleTimeString()}`}
          />
          <StatCard
            title="Umidade Atual do Ar"
            value={`${sensorData?.humidity.current?.value || 0}%`}
            icon={FiDroplet}
            helpText={`Última atualização: ${new Date(sensorData?.humidity.current?.read_at || '').toLocaleTimeString()}`}
          />
          <StatCard
            title="Nível Atual de Gases Tóxicos"
            value={`${sensorData?.toxicGases.current?.value || 0} ppm`}
            icon={FiAlertTriangle}
            helpText={`Última atualização: ${new Date(sensorData?.toxicGases.current?.read_at || '').toLocaleTimeString()}`}
          />
        </SimpleGrid>

        <Box
          w="100%"
          h="calc(100% - 60px)"
          overflowY="auto"
          bg={bgColor}
          p={6}
          borderRadius="lg"
          borderWidth="1px"
          borderColor={borderColor}
          boxShadow="sm"
        >
          {messages.length === 0 ? (
            <Flex
              direction="column"
              align="center"
              justify="center"
              h="100%"
              color="gray.500"
            >
              <Icon as={FaRobot} fontSize="4xl" mb={4} />
              <Text>Inicie uma conversa com o Assistente Virtual</Text>
              <Text fontSize="sm">
                Faça perguntas sobre os dados ambientais e obtenha insights em tempo real
              </Text>
            </Flex>
          ) : (
            messages.map((message, index) => (
              <Flex
                key={index}
                justify={message.role === "user" ? "flex-end" : "flex-start"}
                mb={4}
                align="start"
              >
                {message.role === "assistant" && (
                  <Avatar
                    icon={<FaRobot fontSize="1.2rem" />}
                    bg="blue.500"
                    color="white"
                    size="sm"
                    mr={2}
                  />
                )}
                <Box
                  maxW="70%"
                  bg={message.role === "user" ? messageBgUser : messageBgAssistant}
                  p={4}
                  borderRadius="lg"
                  boxShadow="sm"
                >
                  {message.isLoading ? (
                    <Text
                      as="span"
                      sx={{
                        "&::after": {
                          content: '""',
                          animation: `${loadingDots} 1s steps(4) infinite`,
                        },
                      }}
                    />
                  ) : (
                    <Text whiteSpace="pre-line">{message.content}</Text>
                  )}
                </Box>
                {message.role === "user" && (
                  <Avatar
                    icon={<FaUserCircle fontSize="1.2rem" />}
                    bg="green.500"
                    color="white"
                    size="sm"
                    ml={2}
                  />
                )}
              </Flex>
            ))
          )}
          <div ref={messagesEndRef} />
        </Box>
        
        <InputGroup size="lg">
          <Input
            value={input}
            onChange={(e) => setInput(e.target.value)}
            placeholder="Pergunte sobre os dados da estação climática..."
            onKeyPress={(e) => e.key === "Enter" && handleSend()}
            isDisabled={isChatLoading}
            borderRadius="lg"
            pr="5.5rem"
            _focus={{
              borderColor: "blue.500",
              boxShadow: "0 0 0 1px var(--chakra-colors-blue-500)",
            }}
          />
          <InputRightElement width="4.5rem" mr={2}>
            <Button
              h="1.75rem"
              size="sm"
              onClick={handleSend}
              isLoading={isChatLoading}
              isDisabled={isChatLoading || !input.trim() || !sensorData}
              colorScheme="blue"
              borderRadius="md"
              leftIcon={<FiSend />}
            >
              Send
            </Button>
          </InputRightElement>
        </InputGroup>
      </VStack>
    </Container>
  )
} 