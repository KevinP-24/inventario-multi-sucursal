import jsPDF from 'jspdf';
import autoTable from 'jspdf-autotable';

export function generarComprobanteVentaPdf(
  venta: any, 
  detalles: any[], 
  sucursalNombre: string, 
  responsableNombre: string
): void {
  const doc = new jsPDF();
  
  // Header principal
  doc.setFontSize(22);
  doc.setTextColor(40);
  doc.text('Comprobante de Venta', 14, 22);
  
  // Linea separadora superior
  doc.setLineWidth(0.5);
  doc.setDrawColor(200);
  doc.line(14, 28, 196, 28);
  
  // Datos de la Cabecera
  doc.setFontSize(11);
  doc.setTextColor(60);
  
  // Columna Izquierda
  doc.setFont('helvetica', 'bold');
  doc.text('Sucursal:', 14, 38);
  doc.setFont('helvetica', 'normal');
  doc.text(sucursalNombre, 35, 38);
  
  doc.setFont('helvetica', 'bold');
  doc.text('Comprobante:', 14, 45);
  doc.setFont('helvetica', 'normal');
  doc.text(venta.comprobante, 42, 45);
  
  doc.setFont('helvetica', 'bold');
  doc.text('Fecha:', 14, 52);
  doc.setFont('helvetica', 'normal');
  doc.text(venta.fecha ? venta.fecha.slice(0, 16).replace('T', ' ') : 'N/A', 30, 52);
  
  // Columna Derecha
  doc.setFont('helvetica', 'bold');
  doc.text('Cliente:', 110, 38);
  doc.setFont('helvetica', 'normal');
  doc.text(venta.cliente_nombre || 'Venta de mostrador', 128, 38);
  
  doc.setFont('helvetica', 'bold');
  doc.text('Atiende:', 110, 45);
  doc.setFont('helvetica', 'normal');
  doc.text(responsableNombre, 128, 45);
  
  // Preparar datos de la tabla
  const body = detalles.map(d => [
    d.producto || 'Producto indeterminado',
    Number(d.cantidad).toFixed(2),
    `COP ${Math.floor(Number(d.precio_unitario) || 0).toLocaleString('es-CO')}`,
    `COP ${Math.floor(Number(d.descuento) || 0).toLocaleString('es-CO')}`,
    `COP ${Math.floor(Number(d.subtotal) || 0).toLocaleString('es-CO')}`
  ]);

  // Dibujar tabla con jspdf-autotable
  autoTable(doc, {
    startY: 60,
    head: [['Producto', 'Cantidad', 'Precio Unit.', 'Descuento', 'Subtotal']],
    body: body,
    theme: 'grid',
    headStyles: { fillColor: [184, 115, 51], textColor: 255 }, // Color corporativo tipo bronze/cafe basado en UI
    alternateRowStyles: { fillColor: [250, 250, 250] },
    margin: { left: 14 }
  });

  // Calcular posicion final de la tabla para los totales
  const finalY = (doc as any).lastAutoTable.finalY || 60;
  
  // Linea separadora de los totales
  doc.line(120, finalY + 8, 196, finalY + 8);
  
  // Totales
  doc.setFontSize(11);
  doc.text('Descuento Total:', 120, finalY + 16);
  doc.text(`COP ${Math.floor(Number(venta.descuento_total || 0)).toLocaleString('es-CO')}`, 196, finalY + 16, { align: 'right' });
  
  doc.setFontSize(14);
  doc.setFont('helvetica', 'bold');
  doc.text('TOTAL VENTA:', 120, finalY + 26);
  doc.text(`COP ${Math.floor(Number(venta.total || 0)).toLocaleString('es-CO')}`, 196, finalY + 26, { align: 'right' });
  
  // Pie de pagina
  doc.setFontSize(8);
  doc.setFont('helvetica', 'normal');
  doc.setTextColor(150);
  doc.text('Este documento es soportado por el sistema de Inventario Multi-Sucursal.', 14, 280);
  doc.text('Documento sin valor fiscal a menos que este acompañado de factura resolutiva.', 14, 285);
  
  // Disparar descarga localmente
  doc.save(`${venta.comprobante}.pdf`);
}
