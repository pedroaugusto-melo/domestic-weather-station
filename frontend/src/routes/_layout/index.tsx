import { IconType } from 'react-icons'
import {
  Box,
  Container,
  Text,
  SimpleGrid,
  Stat,
  StatLabel,
  StatNumber,
  StatHelpText,
  Card,
  CardBody,
  Flex,
  Icon,
  Grid,
  GridItem,
  Spinner,
  Center,
} from "@chakra-ui/react"
import { createFileRoute } from "@tanstack/react-router"
import { FiThermometer, FiDroplet, FiAlertTriangle } from "react-icons/fi"
import {
  LineChart,
  Line,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Legend,
  ResponsiveContainer
} from 'recharts'

import useAuth from "../../hooks/useAuth"
import { useSensorData } from '../../hooks/useSensorData'

export const Route = createFileRoute("/_layout/")({
  component: Dashboard,
})

function StatCard({ title, value, icon, helpText }: Props) {
  return (
    <Card>
      <CardBody>
        <Flex justify="space-between" align="center">
          <Stat>
            <StatLabel>{title}</StatLabel>
            <StatNumber>{value}</StatNumber>
            <StatHelpText>{helpText}</StatHelpText>
          </Stat>
          <Icon as={icon} boxSize={8} color="blue.500" />
        </Flex>
      </CardBody>
    </Card>
  )
}

function StatsInfoCard({ title, stats }: StatsProps) {
  return (
    <Card>
      <CardBody>
        <Text fontSize="lg" mb={4} fontWeight="medium">{title}</Text>
        <Flex direction="column" gap={2}>
          <Stat>
            <StatLabel>Média</StatLabel>
            <StatNumber>{stats.avg}</StatNumber>
          </Stat>
          <Stat>
            <StatLabel>Máxima</StatLabel>
            <StatNumber>{stats.max}</StatNumber>
          </Stat>
          <Stat>
            <StatLabel>Mínima</StatLabel>
            <StatNumber>{stats.min}</StatNumber>
          </Stat>
        </Flex>
      </CardBody>
    </Card>
  )
}

function Dashboard() {
  const { user: currentUser } = useAuth()
  const { data: sensorData, isLoading, error } = useSensorData()

  console.log('Raw sensorData:', sensorData);
  console.log('History data:', sensorData?.history);

  if (isLoading) {
    return (
      <Center h="100vh">
        <Spinner size="xl" />
      </Center>
    )
  }

  if (error || !sensorData) {
    return (
      <Center h="100vh">
        <Text color="red.500">Error loading sensor data</Text>
      </Center>
    )
  }

  return (
    <Container maxW="full">
      <Box pt={8} px={4}>
        <Text fontSize="2xl" mb={6}>
          Olá, {currentUser?.full_name || currentUser?.email} 👋🏼
        </Text>

        {/* Top Stats Cards */}
        <SimpleGrid columns={{ base: 1, md: 3 }} spacing={6} mb={8}>
          <StatCard
            title="Temperatura Atual"
            value={`${sensorData.temperature.current?.value || 0}°C`}
            icon={FiThermometer}
            helpText={`Última atualização: ${new Date(sensorData.temperature.current?.timestamp || '').toLocaleTimeString()}`}
          />
          <StatCard
            title="Umidade Atual do Ar"
            value={`${sensorData.humidity.current?.value || 0}%`}
            icon={FiDroplet}
            helpText={`Última atualização: ${new Date(sensorData.humidity.current?.timestamp || '').toLocaleTimeString()}`}
          />
          <StatCard
            title="Nível Atual de Gases Tóxicos"
            value={`${sensorData.toxicGases.current?.value || 0} ppm`}
            icon={FiAlertTriangle}
            helpText={`Última atualização: ${new Date(sensorData.toxicGases.current?.timestamp || '').toLocaleTimeString()}`}
          />
        </SimpleGrid>

        {/* Temperature and Humidity Section */}
        <Grid templateColumns={{ base: "1fr", lg: "2fr 1fr" }} gap={6} mb={8}>
          <Card>
            <CardBody>
              <Text fontSize="lg" mb={4}>Histórico de Temperatura e Umidade</Text>
              <Box h="300px">
                <ResponsiveContainer width="100%" height="100%">
                  <LineChart data={sensorData.history}>
                    <CartesianGrid strokeDasharray="3 3" />
                    <XAxis 
                      dataKey="timestamp"
                      tickFormatter={(timestamp) => new Date(timestamp).toLocaleTimeString()}
                    />
                    <YAxis yAxisId="left" name="Temperatura" />
                    <YAxis yAxisId="right" orientation="right" name="Umidade" />
                    <Tooltip 
                      labelFormatter={(timestamp) => new Date(timestamp).toLocaleString()}
                    />
                    <Legend />
                    <Line 
                      yAxisId="left"
                      type="monotone" 
                      dataKey="temperature" 
                      stroke="#8884d8" 
                      name="Temperatura (°C)" 
                      dot={false}
                    />
                    <Line 
                      yAxisId="right"
                      type="monotone" 
                      dataKey="humidity" 
                      stroke="#82ca9d" 
                      name="Umidade (%)" 
                      dot={false}
                    />
                  </LineChart>
                </ResponsiveContainer>
              </Box>
            </CardBody>
          </Card>
          <Flex direction="column" gap={6}>
            <StatsInfoCard
              title="Estatísticas de Temperatura"
              stats={{
                avg: `${sensorData.temperature.stats.avg.toFixed(1)}°C`,
                max: `${sensorData.temperature.stats.max.toFixed(1)}°C`,
                min: `${sensorData.temperature.stats.min.toFixed(1)}°C`
              }}
            />
            <StatsInfoCard
              title="Estatísticas de Umidade Relativa"
              stats={{
                avg: `${sensorData.humidity.stats.avg.toFixed(1)}%`,
                max: `${sensorData.humidity.stats.max.toFixed(1)}%`,
                min: `${sensorData.humidity.stats.min.toFixed(1)}%`
              }}
            />
          </Flex>
        </Grid>

        {/* Toxic Gases Section */}
        <Grid templateColumns={{ base: "1fr", lg: "2fr 1fr" }} gap={6} mb={6}>
          <Card>
            <CardBody>
              <Text fontSize="lg" mb={4}>Histórico de Gases Tóxicos</Text>
              <Box h="300px">
                <ResponsiveContainer width="100%" height="100%">
                  <LineChart data={sensorData.history}>
                    <CartesianGrid strokeDasharray="3 3" />
                    <XAxis 
                      dataKey="timestamp"
                      tickFormatter={(timestamp) => new Date(timestamp).toLocaleTimeString()}
                    />
                    <YAxis />
                    <Tooltip 
                      labelFormatter={(timestamp) => new Date(timestamp).toLocaleString()}
                    />
                    <Legend />
                    <Line 
                      type="monotone" 
                      dataKey="toxicGases" 
                      stroke="#ff7300" 
                      name="Gases Tóxicos (ppm)" 
                      dot={false}
                    />
                  </LineChart>
                </ResponsiveContainer>
              </Box>
            </CardBody>
          </Card>
          <StatsInfoCard
            title="Estatísticas de Gases Tóxicos"
            stats={{
              avg: `${sensorData.toxicGases.stats.avg.toFixed(1)} ppm`,
              max: `${sensorData.toxicGases.stats.max.toFixed(1)} ppm`,
              min: `${sensorData.toxicGases.stats.min.toFixed(1)} ppm`
            }}
          />
        </Grid>
      </Box>
    </Container>
  )
}