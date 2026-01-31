from django.db import models
from django.utils import timezone

# Create your models here.
class TipoProducto(models.Model):
    nombre = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.nombre


# ------------------------------
#  MODELO: Producto
# ------------------------------
class Producto(models.Model):
    nombre = models.CharField(max_length=100)
    tipo = models.ForeignKey(TipoProducto, on_delete=models.CASCADE)

    cantidad = models.PositiveIntegerField(default=0)
    
    # PRECIO DE VENTA (ya existe)
    valor = models.DecimalField(max_digits=10, decimal_places=2)
    
    # 🆕 PRECIO DE COMPRA (NUEVO)
    valor_compra = models.DecimalField(
        max_digits=10, 
        decimal_places=2,
        verbose_name="Precio de Compra",
        default=0.00  # Valor por defecto
    )
    
    # 🆕 CALCULAR GANANCIA
    @property
    def ganancia_unitaria(self):
        return float(self.valor) - float(self.valor_compra)
    
    @property
    def margen_porcentaje(self):
        if float(self.valor_compra) > 0:
            return round((self.ganancia_unitaria / float(self.valor_compra)) * 100, 2)
        return 0
    
    umbral_alerta = models.PositiveIntegerField(
        default=5,
        verbose_name="Stock Mínimo de Alerta"
    )
    
    fecha_modificacion = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.nombre} ({self.cantidad} unidades)"


class ImagenProducto(models.Model):
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    ruta = models.CharField(max_length=500)
    
    def __str__(self):
        return f"Imagen {self.id} - {self.producto.nombre}"


# ------------------------------
#  MODELO: Cliente
# ------------------------------
class Cliente(models.Model):
    nombre_completo = models.CharField(max_length=200, verbose_name="Nombre y Apellido")
    nombre_local = models.CharField(max_length=200, blank=True, null=True, verbose_name="Nombre del Local")
    
    # 🆕 CUIL/CUIT
    cuil = models.CharField(
        max_length=13, 
        blank=True, 
        null=True, 
        verbose_name="CUIL/CUIT",
        unique=True  # Opcional: si querés que sea único
    )
    
    email = models.EmailField(unique=True, blank=True, null=True)
    telefono = models.CharField(max_length=20, blank=True, null=True)
    direccion = models.TextField(blank=True, null=True)
    fecha_registro = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = "Cliente"
        verbose_name_plural = "Clientes"
        ordering = ['nombre_completo']
    
    def __str__(self):
        if self.nombre_local:
            return f"{self.nombre_completo} - {self.nombre_local}"
        return self.nombre_completo
    

from django.db import models

class Chofer(models.Model):
    """Modelo para gestionar choferes/conductores"""
    nombre_completo = models.CharField(max_length=200, verbose_name="Nombre Completo")
    telefono = models.CharField(max_length=20)
    vehiculo = models.CharField(max_length=100, verbose_name="Vehículo/Patente")

    pin = models.CharField(
        max_length=6,
        verbose_name="PIN",
        help_text="PIN numérico del chofer"
    )

    activo = models.BooleanField(default=True, verbose_name="Activo")
    notas = models.TextField(blank=True, null=True, verbose_name="Notas/Descripción")
    fecha_registro = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Chofer"
        verbose_name_plural = "Choferes"
        ordering = ['nombre_completo']

    def __str__(self):
        return f"{self.nombre_completo} - {self.vehiculo}"

# ------------------------------
#  MODELO: Ventas (CON ESTADOS)
from django.db import models
from django.contrib.auth.models import User

class Ventas(models.Model):
    """
    Pedido/Venta creada por vendedores.
    NO descuenta stock hasta que estado = 'enviada'
    """

    ESTADO_CHOICES = [
        ('pendiente', 'Pendiente'),
        ('confirmada', 'Confirmada'),
        ('enviada', 'Enviada'),      #  Aquí se descuenta stock
        ('entregada', 'Entregada'),
        ('cancelada', 'Cancelada'),
    ]

    # 🆕 Usuario que creó/posteó la venta (cuando está pendiente)
    usuario_creador = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='ventas_creadas',
        verbose_name="Usuario creador"
    )

    cliente = models.ForeignKey(
        Cliente,
        on_delete=models.CASCADE,
        verbose_name="Cliente"
    )

    # Chofer asignado para el envío futuro
    chofer = models.ForeignKey(
        Chofer,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="Chofer Asignado"
    )

    # Fecha y hora programada para el envío
    fecha_envio_programada = models.DateField(
        blank=True,
        null=True,
        verbose_name="Fecha Programada de Envío"
    )

    hora_envio_programada = models.TimeField(
        blank=True,
        null=True,
        verbose_name="Hora Programada de Envío"
    )

    # Estado de la venta
    estado = models.CharField(
        max_length=20,
        choices=ESTADO_CHOICES,
        default='pendiente',
        verbose_name="Estado"
    )

    valor_total = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0
    )

    fecha_creacion = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Fecha de Creación"
    )

    fecha_envio = models.DateTimeField(
        blank=True,
        null=True,
        verbose_name="Fecha Real de Envío"
    )

    # Información adicional
    notas = models.TextField(
        blank=True,
        null=True,
        verbose_name="Notas"
    )

    def save(self, *args, **kwargs):
        # 🔒 Regla de negocio:
        # Una venta en estado pendiente DEBE tener usuario creador
        if self.estado == 'pendiente' and not self.usuario_creador:
            raise ValueError(
                "Una venta en estado pendiente debe tener un usuario creador asignado"
            )

        super().save(*args, **kwargs)

    def __str__(self):
        return f"Venta #{self.id} - {self.cliente} - {self.estado}"
    
    class Meta:
        verbose_name = "Venta"
        verbose_name_plural = "Ventas"
        ordering = ['-fecha_creacion']

    def __str__(self):
        return f"Venta #{self.id} - {self.cliente.nombre_completo} - {self.get_estado_display()}"
    
    def calcular_total(self):
        """Calcula el total sumando todos los detalles"""
        return sum(detalle.subtotal for detalle in self.detalles.all())


class DetalleVenta(models.Model):
    """
    Detalle de productos en la venta
    """
    venta = models.ForeignKey(Ventas, on_delete=models.CASCADE, related_name='detalles')
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    cantidad = models.PositiveIntegerField()
    precio_unitario = models.DecimalField(max_digits=10, decimal_places=2)
    subtotal = models.DecimalField(max_digits=10, decimal_places=2)
    
    class Meta:
        verbose_name = "Detalle de Venta"
        verbose_name_plural = "Detalles de Ventas"
    
    def __str__(self):
        return f"{self.cantidad}x {self.producto.nombre} - ${self.subtotal}"


# ------------------------------
#  MODELO: Envío (OPCIONAL - Para tracking)
# ------------------------------
class Envio(models.Model):
    """
    Modelo OPCIONAL para tracking de envíos.
    Se puede vincular con una Venta.
    """
    
    ESTADO_CHOICES = [
        ('pendiente', 'Pendiente'),
        ('en_camino', 'En Camino'),
        ('entregado', 'Entregado'),
        ('cancelado', 'Cancelado'),
    ]
    
    # Vincula con la venta
    venta = models.OneToOneField(
        Ventas, 
        on_delete=models.CASCADE, 
        related_name='envio',
        verbose_name="Venta"
    )
    
    chofer = models.ForeignKey(Chofer, on_delete=models.SET_NULL, null=True, verbose_name="Chofer Asignado")
    
    # Información del envío
    fecha_envio = models.DateField(verbose_name="Fecha de Envío")
    hora_estimada = models.TimeField(verbose_name="Hora Estimada de Entrega")
    
    # Estado y seguimiento
    estado = models.CharField(max_length=20, choices=ESTADO_CHOICES, default='pendiente')
    hora_real_entrega = models.DateTimeField(blank=True, null=True, verbose_name="Hora Real de Entrega")
    
    # Información adicional
    direccion_entrega = models.TextField(verbose_name="Dirección de Entrega")
    notas = models.TextField(blank=True, null=True, verbose_name="Notas Adicionales")
    
    # Timestamps
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_modificacion = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "Envío"
        verbose_name_plural = "Envíos"
        ordering = ['-fecha_envio', 'hora_estimada']
    
    def __str__(self):
        return f"Envío {self.id} - Venta #{self.venta.id} ({self.fecha_envio})"



from django.db import models
from django.contrib.auth.models import User

class PerfilUsuario(models.Model):
    USUARIO_TIPOS = (
        ('ventas', 'Ventas'),
        ('administrativo', 'Administrativo'),
        ('camiones', 'Camiones'),
     
    )
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    tipo = models.CharField(max_length=20, choices=USUARIO_TIPOS, default='ventas')

    def __str__(self):
        return f"{self.user.username} - {self.get_tipo_display()}"
