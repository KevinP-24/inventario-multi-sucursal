export type ApiErrorValueDto = string | readonly string[];

export interface ApiErrorMapDto {
  readonly [key: string]: ApiErrorValueDto;
}

export interface ApiResponseDto<T> {
  readonly data: T;
  readonly message?: string;
  readonly errors?: ApiErrorMapDto;
}
