import time
import serial
from loguru import logger

from pymodbus.client import ModbusSerialClient 

from .udev_tty import TTYPortFromUsbInfo
from .udev_tty import SerialPortFromUsbSetting

from .modbus_client_base import ConnectorModbusClientBase


class ConnectorModbusClientSerial(ConnectorModbusClientBase):
    """The serial modbus client connector centralize access to a given port as a modbus client
    """

    # Contains instances
    __instances = {}

    ###########################################################################
    ###########################################################################

    @staticmethod
    def GetV2(**kwargs):
        """Singleton main getter
        """

        # Get the serial port name
        port_name = None
        if "port_name" in kwargs:
            port_name = kwargs["port_name"]
        elif "vendor" in kwargs:
            port_name = SerialPortFromUsbSetting(**kwargs)
            kwargs["port_name"] = port_name
        else:
            raise Exception("no way to identify the modbus serial port")


        # Create the new connector
        if not (port_name in ConnectorModbusClientSerial.__instances):
            ConnectorModbusClientSerial.__instances[port_name] = None
            try:
                new_instance = ConnectorModbusClientSerial(**kwargs)
                ConnectorModbusClientSerial.__instances[port_name] = new_instance
            except Exception as e:
                ConnectorModbusClientSerial.__instances.pop(port_name)
                raise Exception('Error during initialization').with_traceback(e.__traceback__)

        # Return the previously created
        return ConnectorModbusClientSerial.__instances[port_name]


    @staticmethod
    def Get(usb_vendor_id: str = None, usb_product_id: str = None, usb_serial_id: str = None, usb_base_dev_tty: str ="/dev/ttyACM",
        port: str = None, baudrate: int = 19200, bytesize: int = 8, parity: chr = 'N', stopbits: int = 1,
        validator=None):
        """Singleton main getter
        """

        # Warning DEPRECATED !!!
        logger.warning("ConnectorModbusClientSerial::Get() deprecated use GetV2()")

        # Get the serial port key
        port_name = None
        if port != None:
            port_name = port
        elif usb_vendor_id != None and usb_product_id != None:
            port_name = TTYPortFromUsbInfo(usb_vendor_id, usb_product_id, usb_serial_id, usb_base_dev_tty)
        else:
            raise Exception("no way to identify the modbus serial port")

        # Create the new connector
        if not (port_name in ConnectorModbusClientSerial.__instances):
            ConnectorModbusClientSerial.__instances[port_name] = None
            try:
                new_instance = ConnectorModbusClientSerial(port_name=port_name, baudrate=baudrate, bytesize=bytesize, parity=parity, stopbits=stopbits, validator=validator)
                ConnectorModbusClientSerial.__instances[port_name] = new_instance
            except Exception as e:
                ConnectorModbusClientSerial.__instances.pop(port_name)
                raise Exception('Error during initialization').with_traceback(e.__traceback__)

        # Return the previously created
        return ConnectorModbusClientSerial.__instances[port_name]

    ###########################################################################
    ###########################################################################

    def __init__(self, **kwargs):
        """Constructor
        """
        key = kwargs["port_name"]

        if not (key in ConnectorModbusClientSerial.__instances):
            raise Exception("You need to pass through Get method to create an instance")
        else:
            self.log = logger.bind(driver_name=key)
            self.log.info(f"attached to the Modbus Serial Client Connector")

            # create client object
            self.client = ModbusSerialClient(
                port=key, 
                baudrate=kwargs.get("baudrate", 9600),
                bytesize=kwargs.get("bytesize", 8),
                parity=kwargs.get("parity", 'N'),
                stopbits=kwargs.get("stopbits", 1)
            )
            # connect to device
            self.client.connect()

            # In case multiple bus match previous conditions
            # TODO need to be improve 
            # if validator:
            #     validator(self)
  



    ###########################################################################
    ###########################################################################

    def write_register(self, address: int, value, unit: int = 1):
        """
        """
        response = self.client.write_register(address, value, unit=unit)
        if response.isError():
            raise Exception(f'Error message: {response}')

    ###########################################################################
    ###########################################################################

    def read_input_registers(self, address: int, size: int = 1, unit: int = 1):
        """
        """
        response = self.client.read_input_registers(address, size, unit=unit)
        if not response.isError():
            return response.registers
        else:
            raise Exception(f'Error message: {response}')

    ###########################################################################
    ###########################################################################

    def read_holding_registers(self, address: int, size: int = 1, unit: int = 1):
        """
        """
        response = self.client.read_holding_registers(address=address, count=size, slave=unit)
        if not response.isError():
            return response.registers
        else:
            raise Exception(f'Error message: {response}')


