<?xml version='1.0' encoding='UTF-8'?>
<esdl:EnergySystem xmlns:esdl="http://www.tno.nl/esdl" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" name="" id="b886e0fa-b998-4158-a77c-b8a4b582358c" description="">
  <instance xsi:type="esdl:Instance" name="Untitled instance" id="d0d51bbd-12b6-4dd8-8655-7074ae4ba735">
    <area xsi:type="esdl:Area" id="eef9190e-89a6-4a25-8a6e-c1653ad9c42b" name="Untitled area">
      <asset xsi:type="esdl:GenericProducer" name="GenericProducer_1188" id="1188a75d-24d7-4460-bd03-0bc2bd93483d" power="1000000.0" prodType="FOSSIL">
        <port xsi:type="esdl:OutPort" carrier="b6896136-6010-42e6-a6f8-f518b1992e32" connectedTo="6f311197-714a-4d6e-9521-66d34eb21052" name="Out" id="383e8bf1-bee3-48a8-b694-443a4aa5f928"/>
        <geometry xsi:type="esdl:Point" lat="53.45902874036418" lon="5.671005249023438" CRS="WGS84"/>
      </asset>
      <asset xsi:type="esdl:GenericProducer" name="GenericProducer_77df" id="77df7f24-3f11-4e0b-8dca-3633cefe0dc5" power="1000000.0" prodType="FOSSIL">
        <port xsi:type="esdl:OutPort" carrier="9ae925af-c191-4932-8ed1-f3e84c5f172d" connectedTo="94659d24-b7ab-4cd1-983c-40638d70f648" name="Out" id="36c0f379-e7d3-4dad-aa6e-1484f7c7800d"/>
        <geometry xsi:type="esdl:Point" lat="53.43715086245288" lon="5.671691894531251" CRS="WGS84"/>
      </asset>
      <asset xsi:type="esdl:HeatingDemand" name="HeatingDemand_6992" id="6992d3af-f3b7-4c91-8d81-67d861df8726">
        <port xsi:type="esdl:InPort" carrier="7c6439be-42df-4f09-8263-a3f1e49ee0ce" name="In" connectedTo="ffa0d830-11de-45c6-8f54-685ae2aec22a 16c06616-b849-4624-8ab4-121657bb1c66" id="2d09f9f3-3567-470f-a229-c654f41cadce">
          <profile xsi:type="esdl:InfluxDBProfile" startDate="2019-01-01T00:00:00.000000+0100" field="G1A" port="8086" filters="" multiplier="50.0" host="http://influxdb" measurement="standard_profiles" id="78eba100-6031-4c08-bad1-de4de1c4a086" endDate="2020-01-01T00:00:00.000000+0100" database="energy_profiles">
            <profileQuantityAndUnit xsi:type="esdl:QuantityAndUnitType" multiplier="GIGA" description="Energy in GJ" physicalQuantity="ENERGY" id="eb07bccb-203f-407e-af98-e687656a221d" unit="JOULE"/>
          </profile>
        </port>
        <geometry xsi:type="esdl:Point" lat="53.45044250555688" lon="5.753059387207032" CRS="WGS84"/>
      </asset>
      <asset xsi:type="esdl:HeatPump" controlStrategy="e618814f-fd30-4449-8bd9-133edb12825e" efficiency="1.0" name="HeatPump_0db0" id="0db0c79a-e7be-47e3-9b50-20f58bd50d77" COP="3.0" power="3000.0">
        <costInformation xsi:type="esdl:CostInformation">
          <marginalCosts xsi:type="esdl:SingleValue" name="HeatPump_0db0-MarginalCosts" id="8d9e7ee6-fff1-4766-b2ef-ab545814f117" value="0.4"/>
        </costInformation>
        <port xsi:type="esdl:InPort" carrier="9ae925af-c191-4932-8ed1-f3e84c5f172d" name="In" connectedTo="36c0f379-e7d3-4dad-aa6e-1484f7c7800d" id="94659d24-b7ab-4cd1-983c-40638d70f648"/>
        <port xsi:type="esdl:OutPort" carrier="7c6439be-42df-4f09-8263-a3f1e49ee0ce" connectedTo="2d09f9f3-3567-470f-a229-c654f41cadce" name="Out" id="16c06616-b849-4624-8ab4-121657bb1c66"/>
        <geometry xsi:type="esdl:Point" lat="53.43899149184269" lon="5.709457397460938"/>
      </asset>
      <asset xsi:type="esdl:GasHeater" controlStrategy="4ddb3f1e-398a-4ac4-b889-13b2b562d00d" efficiency="0.9" name="GasHeater_782c" id="782cc5bf-3f31-45ba-9fb5-6a6d3f1e3acd" power="10000.0">
        <costInformation xsi:type="esdl:CostInformation">
          <marginalCosts xsi:type="esdl:SingleValue" name="GasHeater_782c-MarginalCosts" id="a10dda6f-7e51-4ac6-9d3a-0a25f003567c" value="0.6"/>
        </costInformation>
        <port xsi:type="esdl:InPort" carrier="b6896136-6010-42e6-a6f8-f518b1992e32" name="In" connectedTo="383e8bf1-bee3-48a8-b694-443a4aa5f928" id="6f311197-714a-4d6e-9521-66d34eb21052"/>
        <port xsi:type="esdl:OutPort" carrier="7c6439be-42df-4f09-8263-a3f1e49ee0ce" connectedTo="2d09f9f3-3567-470f-a229-c654f41cadce" name="Out" id="ffa0d830-11de-45c6-8f54-685ae2aec22a"/>
        <geometry xsi:type="esdl:Point" lat="53.45861991140519" lon="5.709114074707032" CRS="WGS84"/>
      </asset>
    </area>
  </instance>
  <energySystemInformation xsi:type="esdl:EnergySystemInformation" id="1fac5c16-7de2-4b06-bd24-e912c51a7f0b">
    <carriers xsi:type="esdl:Carriers" id="e22ad0ae-61b7-4571-9b5e-77aff815fe35">
      <carrier xsi:type="esdl:HeatCommodity" id="7c6439be-42df-4f09-8263-a3f1e49ee0ce" name="Warmte"/>
      <carrier xsi:type="esdl:GasCommodity" id="b6896136-6010-42e6-a6f8-f518b1992e32" name="Aardgas"/>
      <carrier xsi:type="esdl:ElectricityCommodity" id="9ae925af-c191-4932-8ed1-f3e84c5f172d" name="Electricity"/>
    </carriers>
  </energySystemInformation>
  <services xsi:type="esdl:Services">
    <service xsi:type="esdl:DrivenByDemand" energyAsset="0db0c79a-e7be-47e3-9b50-20f58bd50d77" name="DrivenByDemand for HeatPump_0db0" id="e618814f-fd30-4449-8bd9-133edb12825e" outPort="16c06616-b849-4624-8ab4-121657bb1c66"/>
    <service xsi:type="esdl:DrivenByDemand" energyAsset="782cc5bf-3f31-45ba-9fb5-6a6d3f1e3acd" name="DrivenByDemand for GasHeater_782c" id="4ddb3f1e-398a-4ac4-b889-13b2b562d00d" outPort="ffa0d830-11de-45c6-8f54-685ae2aec22a"/>
  </services>
</esdl:EnergySystem>
