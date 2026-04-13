import { ApiResponseDto } from './api-response.dto';

export interface PaginationMetaDto {
  readonly page: number;
  readonly per_page: number;
  readonly total: number;
  readonly total_pages: number;
}

export interface PaginatedResponseDto<T> extends ApiResponseDto<readonly T[]> {
  readonly pagination: PaginationMetaDto;
}
