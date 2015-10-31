In a Body Sensor Network, the sensors information is relayed through relay within reach wirelessly. There is a possibility of relay failure. Considering this a new component PDEP is introduced into fault tolerance literature. 

![BSN](https://github.com/arhik/Probabilistic-Competing-Failures/blob/master/.Images/BAN.jpg)

![components](https://github.com/arhik/Probabilistic-Competing-Failures/blob/master/.Images/BSN_components.jpg)

In this project the wireless motes may fail because of sensor failure or tranmission failures and the components may be isolated. ()

![isolation](https://github.com/arhik/Probabilistic-Competing-Failures/blob/master/.Images/IsolationFacorDetails.png)
The monte-carlo simulation of the above scenario is done to compute its reliability.

The Fault tree diagram of the above description is shown below.

![BaseFT](https://github.com/arhik/Probabilistic-Competing-Failures/blob/master/.Images/BaseFT.png)

The detailed Fault tree describing the component's sensor and transmittor.

![DetailedFT](https://github.com/arhik/Probabilistic-Competing-Failures/blob/master/.Images/DetailedFT.png)

Analytical values from research.

![table](https://github.com/arhik/Probabilistic-Competing-Failures/blob/master/.Images/AnalyticalValuesTable.png)

The Reliability values from the Monte-Carlo simulation of the above context are as follows:

[0.1305, 0.6198, 0.9664, 0.9997]
[0.1037, 0.5386, 0.9532, 0.9999]
[0.1317, 0.5983, 0.958, 0.9998]
[0.1136, 0.5765, 0.9629, 0.9998]
[0.1154, 0.5808, 0.9637, 0.9995]
[0.1103, 0.5558, 0.9529, 0.9996]
[0.1074, 0.5599, 0.9565, 0.9996]

![]