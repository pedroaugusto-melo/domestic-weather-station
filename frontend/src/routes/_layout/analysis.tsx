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
  useColorModeValue,
  Spinner,
  Center,
  Skeleton,
  SkeletonText,
} from "@chakra-ui/react";
import { createFileRoute } from "@tanstack/react-router";
import { FiRefreshCw } from "react-icons/fi";
import { useSensorData } from "../../hooks/useSensorData";
import { useQuery, useQueryClient } from "@tanstack/react-query";
import type { Suggestion } from "../../types/analysis";
import { AnalysisService } from "../../client/services";
export const Route = createFileRoute("/_layout/analysis")({
  component: Analysis,
});

function Analysis() {
  const queryClient = useQueryClient();
  // const { data: sensorData, isLoading: isSensorDataLoading } = useSensorData();
  // mock data
  const sensorData = {
    temperature: { current: { value: 25 } },
    humidity: { current: { value: 50 } },
    toxicGases: { current: { value: 1 } },
  };
  const isSensorDataLoading = false;
  const cardBg = useColorModeValue("white", "gray.800");

  const { 
    data: analysisData, 
    isLoading: isAnalysisLoading, 
    refetch,
    isFetching 
  } = useQuery({
    queryKey: ["analysis", sensorData?.temperature?.current?.value],
    queryFn: () =>
      AnalysisService.getAnalysis(
        sensorData?.temperature?.current?.value || 0,
        sensorData?.humidity?.current?.value || 0,
        sensorData?.toxicGases?.current?.value || 0
      ),
    enabled: !!sensorData,
  });

  const handleRefresh = async () => {
    await queryClient.invalidateQueries({ queryKey: ["sensorData"] });
    refetch();
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

          <Skeleton height="36px" width="250px" />
          <SkeletonText noOfLines={2} spacing="4" skeletonHeight="4" />

          <SimpleGrid columns={{ base: 1, md: 2 }} spacing={6}>
            {[1, 2, 3, 4].map((index) => (
              <Card key={index} bg={cardBg}>
                <CardBody>
                  <Skeleton height="24px" width="200px" mb={4} />
                  <SkeletonText noOfLines={3} spacing="4" skeletonHeight="3" />
                </CardBody>
              </Card>
            ))}
          </SimpleGrid>
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
          alignSelf="flex-end"
          colorScheme="blue"
          isLoading={isFetching}
          loadingText="Atualizando..."
        >
          Atualizar Análise
        </Button>

        <Heading size="lg">Análise Inteligente</Heading>
        <Text>
          Com base nas leituras atuais, nossa IA gerou as seguintes sugestões para
          melhorar seu conforto e segurança:
        </Text>

        <SimpleGrid columns={{ base: 1, md: 2 }} spacing={6}>
          {suggestions.map((suggestion: Suggestion, index: number) => (
            <Card key={index} bg={cardBg}>
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
