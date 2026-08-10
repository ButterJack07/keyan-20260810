# Detection on Navigation Deception Signals Based on INS and GNSS Attitude Measurement
**Shi Rong, Liu Jiang**
*Science and Technology on Electronic Information Control Laboratory, Chengdu, China*
*wyx1819@sina.com*

**Abstract:** The effective detection on satellite deception jamming signals is the precondition of subsequent false signal rejection and accurate location processing. Firstly the process of GNSS attitude measurement and the main navigation deception jamming are briefly explained. The carrier platform with INS and GNSS attitude instrument is considered as the object. The published almanacs of navigation satellites are used. The standard reference directions of navigation satellites signals in the carrier platform coordinate system are calculated by using the attitude parameters from INS. The actual directions of signal arrival from navigation satellites in the process of attitude solution are compared with the reference ones, so as to detect on satellite navigation deception jamming signals effectively. The method makes full use of the natural advantages of GNSS attitude instrument, without any hardware modification about existing equipments, only needs to add the integrated data processing software module. Its wide adaptability and good detection capability are suitable for engineering applications. Finally, the feasibility and availability of the method are verified by the digital simulations. This is not only a new approach for detection on satellite navigation deception jamming signals, but also a new reference for the integrated application of GNSS attitude instrument and INS.

**Keywords:** attitude measurement; direction of signal arrival; direction finding; inertial navigation system; satellite almanac; detection on deception jamming

# 基于惯导与GNSS测姿解算的导航欺骗信号检测
**石荣，刘江**
*电子信息控制重点实验室，成都，中国，610036*
*wyx1819@sina.com*

**【摘要】** 对卫星导航欺骗干扰信号进行有效检测是后续虚假信号剔除与准确定位处理的前提。针对这一需求，在对GNSS姿态仪测姿过程与导航欺骗干扰主要类型简要概述的基础上，以同时装载惯导与GNSS姿态仪的运载平台为研究对象，利用公开发布的导航卫星历书数据，结合惯导输出参数，计算得到各颗导航卫星所发射信号在载体坐标系中的标准参考来波方向，将GNSS姿态仪测姿解算过程中所实际测量到的各导航卫星信号的实际来波方向同标准参考来波方向进行比对，以此来实现对卫星导航欺骗干扰信号的有效检测。该方法充分利用了GNSS姿态仪通过测向来完成测姿的天然优势，不用对现有设备进行任何硬件改造，仅需添加部分数据综合处理软件模块即可在工程中推广应用，适用面广，检测性好。最后通过数字仿真验证了该方法的可行性与有效性，这不仅为卫星导航欺骗干扰信号检测给出了新的途径，同时也为GNSS姿态仪与惯导的综合应用提供了新的参考。

**【关键词】** 姿态测量；信号来波方向；测向；惯导；卫星历书；欺骗信号检测

## 1 引言
全球四大卫星导航系统GPS，GLONASS，BD，Galileo在使用中都面临来自外界干扰的威胁，特别是欺骗干扰给系统上层应用造成了严重影响$^{[1]}$。对卫星导航欺骗信号进行有效检测，确保后续定位处理的可信度是近年来的研究热点$^{[2]}$，目前已提出了一些欺骗干扰的检测方法。例如：基于最短传输路径与信号强度的转发欺骗信号检测$^{[3]}$，基于互相关投影的欺骗干扰抑制方法$^{[4]}$，天线阵载波相位双差的欺骗干扰检测$^{[5]}$，利用调零天线测向与夹角比对的欺骗信号检测$^{[6]}$，基于时钟频漂检验的卫星导航欺骗识别$^{[7]}$，以及两级结构的卫星导航压制式和欺骗式干扰联合抑制算法$^{[8]}$等。其中最有效的是对导航卫星信号进行测向来检测欺骗干扰，因为对于欺骗干扰实施方来讲，可对导航信号的载波频率、调制方式、符号速率、测距伪码等特征进行伪造，但在目前技术条件下唯一难以伪造的信号特征是电磁波的来波方向，这好比电磁信号的DNA，将其在空间中沿直线传播这一本质特性烙印在了电磁波波动传播过程之中。所以对接收机已捕获的导航信号进行来波方向测量，判别该方向的合法性成为卫星导航欺骗干扰信号检测的核心关键依据之一。

虽然单天线导航接收机不具备测向条件而限制了该方法的应用，但对于GNSS姿态仪来讲，自身天然具备对导航卫星信号来波方向测量的有利条件，这为导航信号测向用于信号真实性检验奠定了良好基础。本文在介绍GNSS姿态仪的测姿过程与导航欺骗干扰主要类型的基础上，以同时装载惯导与GNSS姿态仪的运载平台为对象，利用公开发布的导航卫星历书数据，通过惯导输出的位置与姿态参数，计算得到各导航卫星信号在载体坐标系中的标准参考来波方向，将GNSS姿态仪测姿解算过程中实际测量到的各导航卫星信号的方向与标准参考方向进行比对，以此来实现对卫星导航欺骗干扰信号的有效检测。上述方法完全不需要对GNSS姿态仪和惯导做任何硬件改动，而只需在其数据处理软件中增加欺骗干扰检测模块，即能使目前商用GNSS姿态仪具有导航欺骗干扰检测能力，从而为该方法的广泛应用提供了很好的条件。详细阐述如下。

## 2 GNSS 姿态仪的测姿过程
GNSS 姿态仪对来至同一颗导航卫星的信号做载波相位差分测量来实现测向，其原理与电子侦察中相位干涉仪测向是完全相同的。在二维平面条件下通过相位差测量来实现测向的原理如图 1 所示。

![(Figure 1. Direction finding by phase difference measurement 图 1.通过相位差测量来实现测向)](./图片1.png)

图 1 中天线单元 A、B 之间构成测向基线，其直线距离为 $d$，导航信号来波方向与基线法向之间的夹角为 $\theta$，信号波长为 $\lambda$，来至天线单元 A、B 的 2 路信号之间相位差 $\phi$ 如下式所表达：
$$ \phi = 2\pi d \cdot \sin\theta / \lambda \quad (1) $$
获得相位差测量值 $\hat{\phi}$ 后，可计算来波方向 $\hat{\theta}$ 如下：
$$ \hat{\theta} = \arcsin((\hat{\phi} + 2\pi N)\lambda / (2\pi d)) \quad (2) $$
式（1）中相位差 $\phi$ 的取值范围为 $[-\pi, \pi)$，而在通常的 GNSS 姿态仪中 $d >> \lambda/2$，所以式（1）存在相位模糊问题，即多个不同的 $\theta$ 值与同一个 $\phi$ 值产生对应关系，这也是式（2）中在相位差测量值 $\hat{\phi}$ 的基础上增加的 $2\pi N$ 的原因所在。在电子侦察中一般采用多基线干涉仪来解决这一问题，即用短基线来解长基线的相位差模糊，而在 GNSS 姿态测量系统中通常采用单基线，所以只有通过其它方法来解相位差的整周模糊度，如：双频伪距法、模糊度函数法、模糊度协方差法等。图 1 仅仅是用二维情形来说明 GNSS 姿态仪中的测向原理，在实际的三维来波方向测量中，一般在平台上布置相互垂直的 2 条基线来实施平台的姿态测量，如图 2 所示。

![(Figure 2. Attitude measurement by direction finding for navigation satellite signals 图 2.通过对导航信号来波方向测向来解算平台姿态)](./图片2.png)

图 2 中在被测平台上建立载体坐标系，天线 A、B 构成一条基线，记为 $Y_A$ 轴，天线 C、D 构成另一条垂直基线，记为 $X_A$ 轴，$Z_A$ 轴与 $X_A$、$Y_A$ 轴形成右手直角坐标系。图 2 中的载体坐标系可以看成是本地东北天直角坐标系将原点平移到 O 点之后，再通过三维旋转而成，而绕各个轴的旋转参数即决定了平台的姿态参数：航向角 $\alpha_1$，俯仰角 $\alpha_2$，横滚角 $\alpha_3$。如图 2 所示，GNSS 姿态仪可测量得第 $i$ 颗导航卫星在载体坐标系中的来波方向，其对应的单位矢量记为 $\boldsymbol{\beta}_i, i=1;\cdots, M$，$M$ 为可见导航卫星的数目。而该来波方向在本地东北天坐标系中对应的单位矢量为 $\boldsymbol{\gamma}_i$，且 $\boldsymbol{\gamma}_i$ 在完成平台定位之后为已知值，于是可建立如下方程：
$$ \boldsymbol{\beta}_i = \mathbf{M}_3 \cdot \mathbf{M}_2 \cdot \mathbf{M}_1 \cdot \boldsymbol{\gamma}_i \quad (3) $$
其中 $\mathbf{M}_1, \mathbf{M}_2, \mathbf{M}_3$ 表示旋转变换矩阵：
$$
\mathbf{M}_1 = \begin{bmatrix}
\cos\alpha_1 & -\sin\alpha_1 & 0 \\
\sin\alpha_1 & \cos\alpha_1 & 0 \\
0 & 0 & 1
\end{bmatrix} \quad (4)
$$
$$
\mathbf{M}_2 = \begin{bmatrix}
1 & 0 & 0 \\
0 & \cos\alpha_2 & \sin\alpha_2 \\
0 & -\sin\alpha_2 & \cos\alpha_2
\end{bmatrix} \quad (5)
$$
$$
\mathbf{M}_3 = \begin{bmatrix}
\cos\alpha_3 & 0 & -\sin\alpha_3 \\
0 & 1 & 0 \\
\sin\alpha_3 & 0 & \cos\alpha_3
\end{bmatrix} \quad (6)
$$
一般来讲，仅需对 3 颗导航卫星的信号来波方向实施测向即可建立式（3）所示的方程，从而求解出姿态参数 $\alpha_1, \alpha_2, \alpha_3$。在 $M \ge 4$ 的条件下，式（3）中方程的个数将多于未知数的个数，此时可通过最小二乘法进行求解，如式（7）所示。
$$ (\alpha_1, \alpha_2, \alpha_3) = \text{argmin} \sum_{i=1}^{M} \| \boldsymbol{\beta}_i - \mathbf{M}_3 \cdot \mathbf{M}_2 \cdot \mathbf{M}_1 \cdot \boldsymbol{\gamma}_i \|^2 \quad (7) $$

## 3 导航欺骗干扰的主要类型
目前在各类公开发表的文献中报道过的导航欺骗干扰主要有如下两种类型：
1）自主生成式导航欺骗干扰
自主生成式导航欺骗干扰主要是模仿导航卫星生成导航信号的方法来合成欺骗干扰信号。该方法需要按照导航电文中各个字段的含义，编写需要的星历和历书，然后将导航电文按照对应的编码方式、调制样式、符号速率、测距扩频码、载波频率等参数调制成射频信号对目标导航接收机进行辐射。目标导航接收机在接收到此欺骗干扰信号之后，按照正常的导航信号接收流程对该欺骗信号实施捕获、跟踪、解扩、解调等操作，并得到其导航电文，在此基础上计算该欺骗信号对应的虚假导航卫星的位置、速度等参数，并在实施伪距测量之后建立起测距方程，从而最后解算出接收机的位置坐标。显然由这颗虚假导航卫星产生的欺骗信号所建立的测距方程是假的，导航接收机所解算出的位置坐标也是假的，从而达到欺骗干扰的目的。
2）转发式导航欺骗干扰
在自主生成式导航欺骗干扰信号合成中需要已知所有的导航信号参数，这对于民码来讲是可以实现的，因为全球四大卫星导航系统 GPS，GLONASS，BD，Galileo 的民码都是完全公开的，所以对 GNSS 民码的欺骗干扰完全可以采用自主生成式。全球四大卫星导航系统中的军码都是保密的，甚至是加密的，在未知密码的条件下虽然不能对其实施自主生成式导航欺骗干扰，但转发式导航欺骗干扰是不需要太多限制条件的，转发之所以能够实现定位坐标的欺骗，其主要原因在于它对真实导航卫星信号实施了时延控制，而 GNSS 实施定位的基础是准确的伪距测量，从本质上讲伪距测量与时延测量是等价的，于是干扰实施方通过转发导航卫星信号来使得导航接收机产生虚假的伪距测量结果，从而达到欺骗最终定位结果的目的。由于转发式导航欺骗干扰不需要干扰方更加深入地了解导航电文与导航信号的更多参数，所以对于民码导航接收机和军码导航接收机都能实施欺骗干扰。

## 4 惯导与 GNSS 测姿解算的数据比对
在某一时刻，导航卫星在太空中的位置是确定的，而欺骗干扰机在地球上的位置也是确定的。从导航卫星发射的真实导航信号到达导航接收机的方向，以及从欺骗干扰机发射的虚假导航信号到达导航接收机的方向难以在同一个方向上。所以导航接收机通过对已经捕获的导航信号的来波方向进行测向，就能在一定程度上区分该信号是来至真实的导航卫星，还是来至一个虚假的方向。而这正是 GNSS 姿态仪与惯导综合应用的优势所在。

平台上安装的惯导系统不仅输出平台的位置坐标，记为 $(x_{\text{in}}, y_{\text{in}}, z_{\text{in}})$，而且输出平台的姿态参数，记为 $(\alpha_{\text{in } 1}, \alpha_{\text{in } 2}, \alpha_{\text{in } 3})$。虽然上述位置与姿态参数均有一定的误差，但惯导是一种自闭环系统，不会受外界电磁信号干扰，所以在导航反欺骗中可将惯导的数据作为真实性比对的基准。

GNSS 姿态仪的数据处理过程中各颗导航卫星在东北天坐标系中的信号来波方向对应的单位矢量 $\boldsymbol{\gamma}_i$ 的计算需要平台的自身定位坐标，但在完成导航欺骗干扰检测之前，是无法判断当前 GNSS 输出的定位坐标值是否已经受到了欺骗信号的影响。为了避免这一问题，平台自身定位坐标可采用惯导的输出值 $(x_{\text{in}}, y_{\text{in}}, z_{\text{in}})$，而各颗导航卫星的坐标值可以通过公开发布的卫星历书数据计算得到，将其记为 $(x_{\text{s},i}, y_{\text{s},i}, z_{\text{s},i})$，于是参考方向在本地东北天坐标系中的单位矢量 $\boldsymbol{\gamma}_i = (\gamma_{\text{x},i}, \gamma_{\text{y},i}, \gamma_{\text{z},i})^{\text{T}}$ 可由下式计算。
$$
\begin{cases}
\gamma_{\text{x},i} = (x_{\text{s},i} - x_{\text{in}}) / l_i \\
\gamma_{\text{y},i} = (y_{\text{s},i} - y_{\text{in}}) / l_i \\
\gamma_{\text{z},i} = (z_{\text{s},i} - z_{\text{in}}) / l_i \\
l_i = \sqrt{(x_{\text{s},i} - x_{\text{in}})^2 + (y_{\text{s},i} - y_{\text{in}})^2 + (z_{\text{s},i} - z_{\text{in}})^2}
\end{cases} \quad (8)
$$
由于导航卫星的轨道高度一般在 20000km 左右，甚至更高，由式（8）可知，即使惯导输出的定位坐标 $(x_{\text{in}}, y_{\text{in}}, z_{\text{in}})$ 误差达到十几 km，对单位矢量 $\boldsymbol{\gamma}_i$ 的计算精度的影响也是十分微小的。

如前所述，GNSS 姿态仪测量得到第 $i$ 颗导航卫星在载体坐标系中实际信号来波方向对应的单位矢量为 $\hat{\boldsymbol{\beta}}_i$，利用惯导输出的平台真实姿态参数 $(\alpha_{\text{in } 1}, \alpha_{\text{in } 2}, \alpha_{\text{in } 3})$，通过式（1）可反解出在本地东北天坐标系下第 $i$ 颗导航卫星信号实际的来波方向对应的单位矢量 $\hat{\boldsymbol{\gamma}}_{\text{m},i}$ 如下式所表达：
$$ \hat{\boldsymbol{\gamma}}_{\text{m},i} = \mathbf{M}_{\text{m},1}^{-1} \cdot \mathbf{M}_{\text{m},2}^{-1} \cdot \mathbf{M}_{\text{m},3}^{-1} \cdot \hat{\boldsymbol{\beta}}_i \quad (9) $$
式（9）中 $\mathbf{M}_{\text{m},1}, \mathbf{M}_{\text{m},2}, \mathbf{M}_{\text{m},3}$ 分别是与式（4）、（5）、（6）表达类似的旋转矩阵，仅仅是将参数 $\alpha_{\text{in } 1}, \alpha_{\text{in } 2}, \alpha_{\text{in } 3}$ 替代参数 $\alpha_1, \alpha_2, \alpha_3$ 而已。如果实际测量得到的来波方向矢量 $\hat{\boldsymbol{\gamma}}_{\text{m},i}$ 与根据卫星历书所计算出的标准参考来波方向矢量 $\boldsymbol{\gamma}_i$ 之间的误差在门限范围之内，即满足下式，则判为正常。
$$ 2 \cdot \arcsin(\| \hat{\boldsymbol{\gamma}}_{\text{m},i} - \boldsymbol{\gamma}_i \| / 2) \le \gamma_{\text{T}} \quad (10) $$
式（10）中 $\gamma_{\text{T}}$ 为判决门限，该门限可由历书误差与惯导测姿误差联合决定，式（10）中不等式左端运算的物理含义是求取 2 个单位矢量之间的夹角。如果式（10）成立，则可认为该信号是来至一颗真实导航卫星所发射的信号；反之，如果误差超过了门限，则完全有理由判定：该信号来至一个虚假的方向，于是可将该虚假信号剔除，使其不会参与到后续的伪距测量与定位坐标解算的环节，从而达到排除欺骗干扰信号的目的。

## 5 仿真验证
仿真对象设置为 2017 年 9 月 20 日下午 3 点行驶于中国南海的一艘舰船，该舰船上安装有 GPS 姿态仪与惯导系统。惯导输出的定位坐标为：东经 113.6°，北纬 12.8°，高度 26m；惯导输出的姿态参数为：航向角 69.8°，俯仰角 2.5°，横滚角 1.7°。在该地区中有 3 个机载 GPS 干扰机（编号从 1 至 3）分别从方位角 104°，226°，321°三个不同方向对该舰船实施导航欺骗干扰，如图 3 所示。其中 1 号至 3 号干扰机所发射的欺骗干扰信号对应的 GPS 卫星的伪码号 PRN 分别为：29，16，5。

![(Figure 3. Position of the ship and jammers in the map 图 3. 舰船平台与干扰机在地图上所在的位置)](./图片3.png)

此时舰船上的 GPS 姿态仪一共接收到 11 颗 GPS 卫星的信号，在载体坐标系中所测量得到的上述 11 个信号的来波方向所对应的单位矢量 $\hat{\boldsymbol{\beta}}_i$ 如表 1 所示。表中 PRN 表示各颗 GPS 卫星的伪码号。

**Table 1. Unit vector for angle of arrival for GPS satellites**

| 序号 | PRN | 来波方向对应的单位矢量 $\hat{\boldsymbol{\beta}}_i$ |
| :--- | :--- | :--- |
| 1 | 5 | -0.9464,-0.3181,0.0557 |
| 2 | 10 | 0.2861,-0.0793,0.9549 |
| 3 | 14 | -0.8141,0.1522,0.5604 |
| 4 | 16 | 0.3991,-0.9088,0.1214 |
| 5 | 18 | 0.7347,0.0436,0.6770 |
| 6 | 21 | 0.9893,-0.0547,0.1353 |
| 7 | 25 | -0.4157,0.7286,0.5443 |
| 8 | 26 | 0.4835,-0.5410,0.6882 |
| 9 | 29 | 0.5595,0.8273,0.0503 |
| 10 | 31 | -0.6443,-0.3431,0.6835 |
| 11 | 32 | -0.6271,0.3878,0.6756 |

根据一个月前即 2017 年 8 月 20 日网上公开发布的 GPS 历书数据，该舰船可推算出在 2017 年 9 月 20 日下午 3 点在该地点可见的天上各颗 GPS 卫星所发射信号的标准参考来波方向在本地东北天坐标系中的单位矢量 $\boldsymbol{\gamma}_i$ 如表 2 所示。为了进行历书时效性对比，同时根据 2017 年 9 月 20 日当天网上公开发布的 GPS 历书数据，推算出该时刻在该地点各颗 GPS 卫星所发射信号的标准参考来波方向在本地东北天坐标系中的单位矢量 $\boldsymbol{\gamma}_i$ 同时列入表 2 中。通过对比可知，在 GPS 卫星信号的来波方向计算中，采用一个月以前的历书与当前历书所计算出的来波方向最大误差不超过 0.2°。这为本方法的应用提供了极大便利，因为 GPS 历书每天都会在互联网上公开发布，即使 GNSS 姿态仪只存储了一个月以前的历书，这对本文方法的应用影响不大。

**Table 2. Unit vector for standard reference angle of arrival for GPS satellites**

| 序号 | PRN | 来波方向对应的单位矢量(一月前历书) | 来波方向对应的单位矢量(当天历书) |
| :--- | :--- | :--- | :--- |
| 1 | 10 | -0.0030,-0.3362,0.9418 | -0.0022,-0.3386,0.9409 |
| 2 | 14 | -0.1536,0.7911,0.5921 | -0.1551,0.7916,0.5910 |
| 3 | 16 | -0.4576,-0.8680,0.1925 | -0.4585,-0.8678,0.1919 |
| 4 | 18 | 0.2762,-0.7030,0.6554 | 0.2763,-0.7040,0.6543 |
| 5 | 21 | 0.2841,-0.9545,0.0911 | 0.2859,-0.9540,0.0902 |
| 6 | 25 | 0.5222,0.6191,0.5866 | 0.5228,0.6207,0.5843 |
| 7 | 26 | -0.3578,-0.6726,0.6478 | -0.3590,-0.6724,0.6473 |
| 8 | 29 | 0.9309,-0.2358,0.2789 | 0.9313,-0.2345,0.2786 |
| 9 | 31 | -0.5637,0.4551,0.6893 | -0.5661,0.4530,0.6887 |
| 10 | 32 | 0.1300,0.6923,0.7098 | 0.1287,0.6932,0.7092 |

**表 2. 各颗GPS卫星的标准参考来波方向的单位矢量**
对比表 1 与表 2 可知，在该时刻的该地点上不应该出现 PRN 号为 5 的 GPS 卫星信号，由此立即可判断该信号一定为欺骗信号，马上将其剔除，不参与后续的处理环节。在此基础上，将剩余的 10 个 GPS 卫星信号的实际来波方向按照式（9）从载体坐标系转换到本地东北天坐标系，并与表 2 所示的标准参考来波方向进行比对，相应的方向性角度误差如表 3 所示。

**Table 3. Actual angle of arriving vs. standard reference one**

| 序号 | PRN | 转换后单位矢量 $\hat{\boldsymbol{\gamma}}_{\text{m},i}$ | 误差/° |
| :--- | :--- | :--- | :--- |
| 1 | 10 | -0.0045,-0.3366,0.9416 | 0.0902 |
| 2 | 14 | -0.1565,0.7918,0.5904 | 0.1930 |
| 3 | 16 | -0.7176,-0.6930,0.0698 | 19.1063 |
| 4 | 18 | 0.2746,-0.7092,0.6562 | 0.0971 |
| 5 | 21 | 0.2872,-0.9523,0.1034 | 0.7336 |
| 6 | 25 | 0.5224,0.6178,0.5877 | 0.0970 |
| 7 | 26 | -0.3609,-0.6695,0.6493 | 0.2652 |
| 8 | 29 | 0.9679,-0.2413,0.0698 | 12.1304 |
| 9 | 31 | -0.5658,0.4565,0.6866 | 0.2108 |
| 10 | 32 | 0.1257,0.6928,0.7101 | 0.2450 |

**表 3. 实际来波方向与标准参考来波方向的比对**
惯导的测姿精度优于 0.2°，GNSS 的来波方向测量精度优于 0.02°，同时考虑到所使用的 GPS 历书的时效性以及部分判决余量，判决门限可取为 1°。于是将表 3 中的误差数据按照式（10）进行判决，即可发现 PRN 为 16 和 29 号的卫星信号为异常方向入射信号，遂判决为欺骗干扰信号。将上述信号剔除之后，采用剩余的 8 个 GPS 卫星信号作为后续精确定位、授时、测速和测姿的信号来源。

## 6 结束语
虽然单天线卫星导航接收机不具备信号测向能力，但在 GNSS 姿态仪使用过程中，本身就自带当前接收机所捕获到的各个导航信号的实际来波方向信息，所以可直接利用 GNSS 姿态仪的这一天然优势，以惯导输出的定位定姿参数与导航卫星历书数据所确定的标准来波方向作为参考，通过方向比对来完成导航欺骗信号的检测。在目前所使用 GNSS 姿态仪中仅需增加部分检测软件模块，而无需更改任何硬件即可应用这一方法。这不仅为卫星导航欺骗干扰信号检测给出了新的途径，同时也为 GNSS 姿态仪与惯导的综合应用提供了新的参考。

## References (参考文献)
[1] Peter teunissen, Oliver montenbruck. Handbook of global navigation satellite systems [M]. Germany: springer, 2017.
[2] Zhou Xuan, Li Guangxia, Cai Dingbo, et al. Review and Prospect of GNSS Anti-spoofing Techniques [J], *Journal of Navigation and Positioning*, 2013, 1(3), P83-88(Ch). 周轩，李广侠，蔡锭波，等，卫星导航系统防欺骗技术的回顾与展望 [J]，导航定位学报，2013, 1(3), P83-88.
[3] Shi Rong, He Juncen, Xu Jiantao. Detection on Repeater Deception Signal Based on the Shortest Transmission Path and Signal Power [C], *CSNC2017, shanghai*, P1-5(Ch). 石荣，何俊岑，徐剑韬. 基于最短传输路径与信号强度的转发欺骗信号检测[C]. 2017年第八届中国卫星导航学术年会论文集，上海，2017:1-5.
[4] Wang Chun, Zhang Linrang. Spoofing Mitigation Method for Navigation Receiver based on Cross Correlation and Projection [J]. *Journal of Electronics & Information Technique*, 2016, 38(8), P1984-1990(Ch). 王纯，张林让. 基于互相关投影导航接收机欺骗干扰抑制方法[J]. 电子与信息学报，2016, 38(8), P1984-1990.
[5] Zhang Xin, Pang Jing, Su Yingxue, et al. Spoofing detection technique on antenna array carrier phase double difference [J]. *Journal of National University of Defense Technology*, 2014, 36(4), P55-60(Ch). 张鑫，庞晶，苏映雪，等. 天线阵载波相位双差的欺骗干扰检测技术[J]. 国防科技大学学报，2014, 36(4), P55-60.
[6] Shi Rong, Xu Jiantao, Yan Jian. Detection on Navigation Deception Signals based on Direction Finding by Nulling Antenna and Angle Contrast [J]. *Modern Navigation*, 2017, 8 (3), P193-198 (Ch). 石荣，徐剑韬，阎剑. 利用调零天线测向与夹角比对的导航欺骗信号检测[J]. 现代导航，2017, 8 (3), P193-198.
[7] Hu Yanfeng, Cao Kejin, Bian Shaofeng, et al. GNSS spoofing detection algorithm based on clock frequency drift monitoring [J]. *Systems Engineering and Electronics*, 37(7), P1629-1632 (Ch). 胡彦逢，曹可劲，边少锋，等. 基于时钟频漂检验的卫星导航欺骗识别算法[J]. 系统工程与电子技术，2015, 37(7), P1629-1632.
[8] Bao Lina, Wu Renbiao, Wang Wenyi, et al. Two-step GPS Interference Suppression Algorithm for Spoofing and Jamming [J]. *Signal Processing*, 2015, 31(9), P1041-1046(Ch). 包莉娜，吴仁彪，王文益，等. 两级结构的卫星导航压制式和欺骗式干扰联合抑制算法[J]. 信号处理，2015, 31(9), P1041-1046.