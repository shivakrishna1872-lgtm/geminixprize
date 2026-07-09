export type AiGenerationRequest = Readonly<{
  systemInstruction: string;
  userPrompt: string;
  responseSchemaName: string;
}>;

export type AiGenerationResponse = Readonly<{
  text: string;
  model: string;
}>;

export interface AiGenerationService {
  generate(request: AiGenerationRequest): Promise<AiGenerationResponse>;
}
