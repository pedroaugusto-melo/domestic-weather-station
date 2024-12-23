import {
  Box,
  Container,
  Text,
  SimpleGrid,
  Card,
  CardBody,
  Flex,
  Grid,
  Spinner,
  Center,
} from "@chakra-ui/react";
import { createFileRoute } from "@tanstack/react-router";
import { FiThermometer, FiDroplet, FiAlertTriangle } from "react-icons/fi";
import {
  LineChart,
  Line,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Legend,
  ResponsiveContainer,
} from "recharts";

import { TimeRangeSelector } from "../../components/TimeRangeSelector";
import { useState } from "react";
import useAuth from "../../hooks/useAuth";
import { useSensorData } from "../../hooks/useSensorData";
import { StatCard } from "../../components/Common/StatCard";

export const Route = createFileRoute("/_layout/")({
  component: Dashboard,
});

interface StatsProps {
  title: string;
  stats: {
    avg: string;
    max: string;
    min: string;
  };
}

function StatsInfoCard({ title, stats }: StatsProps) {
  return (
    <Card>
      <CardBody>
        <Text fontSize="lg" mb={4} fontWeight="medium">
          {title}
        </Text>
        <Flex direction="column" gap={2}>
          <Text>
            <Text as="span" fontWeight="bold">
              Média:{" "}
            </Text>
            {stats.avg}
          </Text>
          <Text>
            <Text as="span" fontWeight="bold">
              Máxima:{" "}
            </Text>
            {stats.max}
          </Text>
          <Text>
            <Text as="span" fontWeight="bold">
              Mínima:{" "}
            </Text>
            {stats.min}
          </Text>
        </Flex>
      </CardBody>
    </Card>
  );
}

function Dashboard() {
  const [timeRange, setTimeRange] = useState(5);
  const { data: sensorData, isLoading, error } = useSensorData(5000, timeRange);
  const { user: currentUser } = useAuth();

  const formatXAxisTimeStampLabel = (timestamp: number) => {
    const date = new Date(timestamp);

    if (timeRange <= 24 * 60) return date.toLocaleTimeString();
    return date.toLocaleDateString();
  };

  if (isLoading) {
    return (
      <Center w="100%">
        <Spinner size="xl" />
      </Center>
    );
  }

  if (error || !sensorData) {
    return (
      <Center h="100vh">
        <Text color="red.500">Error loading sensor data</Text>
      </Center>
    );
  }

  return (
    <Container maxW="full">
      <Box pt={8} px={4} mt={10}>
        <Flex justify="space-between" align="center" mb={6}>
          <Text fontSize="2xl">
            Olá, {currentUser?.full_name || currentUser?.email} 👋🏼
          </Text>
          <TimeRangeSelector value={timeRange} onChange={setTimeRange} />
        </Flex>

        <SimpleGrid columns={{ base: 1, md: 3 }} spacing={6} mb={8}>
          <StatCard
            title="Temperatura Atual"
            value={`${sensorData.temperature.current?.value || 0}°C`}
            icon={FiThermometer}
            helpText={`Última atualização: ${new Date(sensorData.temperature.current?.read_at || "").toLocaleTimeString()}`}
          />
          <StatCard
            title="Umidade Atual do Ar"
            value={`${sensorData.humidity.current?.value || 0}%`}
            icon={FiDroplet}
            helpText={`Última atualização: ${new Date(sensorData.humidity.current?.read_at || "").toLocaleTimeString()}`}
          />
          <StatCard
            title="Nível Atual de Gases Tóxicos"
            value={`${sensorData.toxicGases.current?.value || 0} ppm`}
            icon={FiAlertTriangle}
            helpText={`Última atualização: ${new Date(sensorData.toxicGases.current?.read_at || "").toLocaleTimeString()}`}
          />
        </SimpleGrid>

        <Grid templateColumns={{ base: "1fr", lg: "2fr 1fr" }} gap={6} mb={8}>
          <Card>
            <CardBody>
              <Text fontSize="lg" mb={4}>
                Histórico de Temperatura e Umidade
              </Text>
              <Box h="300px">
                <ResponsiveContainer width="100%" height="100%">
                  <LineChart data={sensorData.history}>
                    <CartesianGrid strokeDasharray="3 3" />
                    <XAxis
                      dataKey="timestamp"
                      tickFormatter={(timestamp) =>
                        formatXAxisTimeStampLabel(timestamp)
                      }
                    />
                    <YAxis yAxisId="left" name="Temperatura" />
                    <YAxis yAxisId="right" orientation="right" name="Umidade" />
                    <Tooltip
                      labelFormatter={(timestamp) =>
                        formatXAxisTimeStampLabel(timestamp)
                      }
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
          <Box>
            <Flex direction="column" gap={6}>
              <StatsInfoCard
                title="Estatísticas de Temperatura"
                stats={{
                  avg: `${sensorData.temperature.stats.avg.toFixed(1)}°C`,
                  max: `${sensorData.temperature.stats.max.toFixed(1)}°C`,
                  min: `${sensorData.temperature.stats.min.toFixed(1)}°C`,
                }}
              />
              <StatsInfoCard
                title="Estatísticas de Umidade Relativa"
                stats={{
                  avg: `${sensorData.humidity.stats.avg.toFixed(1)}%`,
                  max: `${sensorData.humidity.stats.max.toFixed(1)}%`,
                  min: `${sensorData.humidity.stats.min.toFixed(1)}%`,
                }}
              />
            </Flex>
          </Box>
        </Grid>

        <Grid templateColumns={{ base: "1fr", lg: "2fr 1fr" }} gap={6} mb={6}>
          <Card>
            <CardBody>
              <Text fontSize="lg" mb={4}>
                Histórico de Gases Tóxicos
              </Text>
              <Box h="300px">
                <ResponsiveContainer width="100%" height="100%">
                  <LineChart data={sensorData.history}>
                    <CartesianGrid strokeDasharray="3 3" />
                    <XAxis
                      dataKey="timestamp"
                      tickFormatter={(timestamp) =>
                        formatXAxisTimeStampLabel(timestamp)
                      }
                    />
                    <YAxis />
                    <Tooltip
                      labelFormatter={(timestamp) =>
                        formatXAxisTimeStampLabel(timestamp)
                      }
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
          <Box>
            <StatsInfoCard
              title="Estatísticas de Gases Tóxicos"
              stats={{
                avg: `${sensorData.toxicGases.stats.avg.toFixed(1)} ppm`,
                max: `${sensorData.toxicGases.stats.max.toFixed(1)} ppm`,
                min: `${sensorData.toxicGases.stats.min.toFixed(1)} ppm`,
              }}
            />
          </Box>
        </Grid>
      </Box>
    </Container>
  );
}
