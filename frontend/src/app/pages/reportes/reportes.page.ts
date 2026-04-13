import { CommonModule } from '@angular/common';
import { HttpErrorResponse } from '@angular/common/http';
import { ChangeDetectionStrategy, Component, DestroyRef, inject, signal } from '@angular/core';
import { takeUntilDestroyed } from '@angular/core/rxjs-interop';
import { FormBuilder, ReactiveFormsModule } from '@angular/forms';
import { finalize } from 'rxjs';

import { ReportesApiService } from '../../core/services/reportes/reportes-api.service';
import { SucursalDto } from '../../core/services/sucursales/dtos/sucursal.dto';
import { SucursalesApiService } from '../../core/services/sucursales/sucursales-api.service';
import { PageHeaderComponent } from '../../shared/components/page-header/page-header.component';

type ReporteKind = 'inventario' | 'ventas' | 'transferencias';

@Component({
  selector: 'app-reportes-page',
  standalone: true,
  imports: [CommonModule, ReactiveFormsModule, PageHeaderComponent],
  templateUrl: './reportes.page.html',
  styleUrl: './reportes.page.css',
  changeDetection: ChangeDetectionStrategy.OnPush
})
export class ReportesPage {
  private readonly fb = inject(FormBuilder);
  private readonly destroyRef = inject(DestroyRef);
  private readonly reportesApi = inject(ReportesApiService);
  private readonly sucursalesApi = inject(SucursalesApiService);

  protected readonly loading = signal(false);
  protected readonly downloadingReport = signal<ReporteKind | null>(null);
  protected readonly errorMessage = signal('');
  protected readonly successMessage = signal('');
  protected readonly sucursales = signal<SucursalDto[]>([]);

  protected readonly filtrosForm = this.fb.nonNullable.group({
    id_sucursal: [0],
    fecha_desde: [''],
    fecha_hasta: ['']
  });

  constructor() {
    this.cargarSucursales();
  }

  protected descargarReporte(kind: ReporteKind): void {
    const filtros = this.filtrosForm.getRawValue();
    const payload = {
      id_sucursal: Number(filtros.id_sucursal || 0) || undefined,
      fecha_desde: filtros.fecha_desde || undefined,
      fecha_hasta: filtros.fecha_hasta || undefined
    };

    const request =
      kind === 'inventario'
        ? this.reportesApi.exportarInventarioPdf(payload)
        : kind === 'ventas'
          ? this.reportesApi.exportarVentasPdf(payload)
          : this.reportesApi.exportarTransferenciasPdf(payload);

    this.downloadingReport.set(kind);
    this.errorMessage.set('');
    this.successMessage.set('');

    request
      .pipe(
        finalize(() => this.downloadingReport.set(null)),
        takeUntilDestroyed(this.destroyRef)
      )
      .subscribe({
        next: (blob) => {
          const filename = `reporte-${kind}-${new Date().toISOString().slice(0, 10)}.pdf`;
          this.downloadBlob(blob, filename);
          this.successMessage.set('Reporte generado correctamente.');
        },
        error: (error: HttpErrorResponse) => {
          const apiError = error.error as { message?: string } | null;
          this.errorMessage.set(apiError?.message || 'No se pudo generar el reporte seleccionado.');
        }
      });
  }

  private cargarSucursales(): void {
    this.loading.set(true);

    this.sucursalesApi
      .listarSucursales()
      .pipe(
        finalize(() => this.loading.set(false)),
        takeUntilDestroyed(this.destroyRef)
      )
      .subscribe({
        next: (response) => {
          this.sucursales.set(response.data);
        },
        error: () => {
          this.errorMessage.set('No se pudieron cargar las sucursales para filtrar reportes.');
        }
      });
  }

  private downloadBlob(blob: Blob, filename: string): void {
    const url = URL.createObjectURL(blob);
    const anchor = document.createElement('a');
    anchor.href = url;
    anchor.download = filename;
    anchor.click();
    URL.revokeObjectURL(url);
  }
}
