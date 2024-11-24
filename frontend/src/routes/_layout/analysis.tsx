import {
  Container,
  VStack,
  Heading,
  Text,
  Card,
  CardBody,
  SimpleGrid,
  Button,
  Icon,
  Spinner,
  Center,
} from "@chakra-ui/react";
import { createFileRoute } from "@tanstack/react-router";
import {
  FiRefreshCw,
  FiThermometer,
  FiDroplet,
  FiAlertTriangle,
} from "react-icons/fi";
import { useSensorData } from "../../hooks/useSensorData";
import { useQuery, useQueryClient } from "@tanstack/react-query";
import type { Suggestion } from "../../types/analysis";
import { AnalysisService } from "../../client/services";
import { StatCard } from "../../components/Common/StatCard";

export const Route = createFileRoute("/_layout/analysis")({
  component: Analysis,
});

function Analysis() {
  const queryClient = useQueryClient();
  const { data: sensorData, isLoading: isSensorDataLoading } = useSensorData(0);

  const {
    data: analysisData,
    isLoading: isAnalysisLoading,
    refetch,
    isFetching,
  } = useQuery({
    queryKey: [
      "analysis",
      sensorData?.temperature.current?.value,
      sensorData?.humidity.current?.value,
      sensorData?.toxicGases.current?.value,
    ],
    queryFn: () =>
      AnalysisService.getAnalysis(
        sensorData?.temperature.current?.value || 0,
        sensorData?.humidity.current?.value || 0,
        sensorData?.toxicGases.current?.value || 0
      ),
    enabled: !!sensorData?.temperature.current?.value,
    refetchInterval: undefined,
    refetchOnWindowFocus: false,
  });

  const handleRefresh = async () => {
    await queryClient.invalidateQueries({ queryKey: ["sensorData"] });
    await refetch();
  };

  if (isSensorDataLoading || isAnalysisLoading) {
    return (
      <Container maxW="container.xl" py={8}>
        <VStack spacing={8} align="stretch">
          <Button
            leftIcon={<Icon as={FiRefreshCw} />}
            isLoading
            alignSelf="flex-end"
            colorScheme="blue"
          >
            Atualizar Análise
          </Button>
          <Heading size="lg">Análise Inteligente</Heading>
          <Center p={8}>
            <Spinner size="xl" />
          </Center>
        </VStack>
      </Container>
    );
  }

  const suggestions = JSON.parse(analysisData?.suggestions || "[]");

  return (
    <Container maxW="container.xl" py={8}>
      <VStack spacing={8} align="stretch">
        <Button
          leftIcon={<Icon as={FiRefreshCw} />}
          onClick={handleRefresh}
          isLoading={isFetching}
          alignSelf="flex-end"
          colorScheme="blue"
        >
          Atualizar Análise
        </Button>

        <Heading size="lg">Análise Inteligente</Heading>

        <SimpleGrid columns={{ base: 1, md: 3 }} spacing={6}>
          <StatCard
            title="Temperatura Atual"
            value={`${sensorData?.temperature.current?.value || 0}°C`}
            icon={FiThermometer}
            helpText={`Última atualização: ${new Date(sensorData?.temperature.current?.read_at || "").toLocaleTimeString()}`}
          />
          <StatCard
            title="Umidade Atual do Ar"
            value={`${sensorData?.humidity.current?.value || 0}%`}
            icon={FiDroplet}
            helpText={`Última atualização: ${new Date(sensorData?.humidity.current?.read_at || "").toLocaleTimeString()}`}
          />
          <StatCard
            title="Nível Atual de Gases Tóxicos"
            value={`${sensorData?.toxicGases.current?.value || 0} ppm`}
            icon={FiAlertTriangle}
            helpText={`Última atualização: ${new Date(sensorData?.toxicGases.current?.read_at || "").toLocaleTimeString()}`}
          />
        </SimpleGrid>

        <Text>
          Com base nas leituras atuais, nossa IA gerou as seguintes sugestões
          para melhorar seu conforto e segurança:
        </Text>

        <SimpleGrid columns={{ base: 1, md: 2 }} spacing={6}>
          {suggestions.map((suggestion: Suggestion, index: number) => (
            <Card key={index}>
              <CardBody>
                <Heading size="md" mb={2}>
                  {suggestion.title}
                </Heading>
                <Text>{suggestion.description}</Text>
              </CardBody>
            </Card>
          ))}
        </SimpleGrid>
      </VStack>
    </Container>
  );
}
