import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import scipy as sp

def main():


    mixed = [[2459, 3199, 3283, 2956, 3847, 2282, 2467, 3606, 3594, 3546, 3610, 1770, 3157, 2850, 2148, 2883, 3027, 2310, 3025, 2684], [4098, 3351, 3111, 4147, 3243, 3419, 3838, 3634, 3257, 3367, 3086, 3704, 3859, 2920, 3049, 3891, 3883, 2804, 4162, 3126], [4150, 4160, 4176, 3821, 4122, 4136, 4154, 3594, 4174, 4167, 3659, 3832, 3673, 4162, 3860, 4162, 4196, 3652, 3797, 3947], [4186, 4130, 3497, 4140, 4188, 4172, 4109, 3997, 4152, 4158, 4147, 4162, 4171, 4165, 4136, 4159, 4123, 4122, 4184, 4128], [4117, 4147, 4161, 4148, 4209, 3309, 4102, 4149, 4172, 3343, 4156, 4145, 4130, 4037, 4166, 4157, 4177, 4140, 4181, 4183], [4134, 4149, 4152, 4154, 3005, 4157, 4187, 4167, 4173, 4135, 4153, 2969, 4209, 4155, 4150, 4148, 4149, 2832, 4188, 4161], [4172, 4164, 4160, 4179, 4177, 4193, 2524, 4197, 4205, 3053, 4149, 4146, 4177, 4142, 4176, 4150, 4175, 4173, 3100, 4208], [4211, 4188, 4167, 4143, 4169, 4197, 4172, 3920, 3940, 3724, 4209, 4135, 4229, 3894, 4202, 4174, 2926, 4110, 4164, 4139], [4169, 4186, 4170, 4192, 4133, 4013, 4165, 4154, 4162, 4204, 4166, 4190, 3614, 3396, 4178, 4152, 4170, 4158, 4116, 4167], [4149, 4156, 4159, 4162, 4202, 4171, 4142, 4166, 4180, 4187, 4133, 4162, 4087, 4181, 4182, 4148, 4139, 4147, 4195, 3238], [4100, 4168, 3471, 3803, 4111, 3710, 3592, 4162, 4196, 3367, 4137, 4200, 4174, 4156, 3600, 3561, 4171, 4186, 4184, 4113], [4185, 3255, 3446, 3807, 4173, 4191, 3998, 4147, 4159, 4185, 3910, 3813, 4187, 3845, 4155, 3807, 3040, 4174, 4154, 4127], [4151, 4195, 4145, 4189, 4217, 3685, 4151, 3903, 3322, 4172, 4151, 4195, 4136, 4161, 4153, 4157, 4184, 2924, 4157, 3378], [3570, 4153, 4169, 3773, 3982, 4140, 3783, 4167, 4150, 4145, 4166, 4150, 4194, 4163, 4182, 3784, 4153, 4163, 4158, 4179], [4150, 4157, 4230, 4170, 4148, 4177, 4179, 4183, 3235, 4178, 4156, 4173, 4154, 4159, 3370, 4142, 4145, 4169, 3246, 4196], [4137, 4159, 4028, 4229, 4139, 4113, 4185, 4215, 4165, 4161, 4137, 4179, 3891, 3368, 4184, 4179, 4164, 4149, 4210, 4176], [4147, 4152, 4138, 4155, 4138, 4175, 4149, 4209, 4175, 4145, 3724, 4149, 4197, 3797, 3582, 4125, 4147, 4187, 4193, 4157], [4158, 4196, 4166, 3807, 4204, 4173, 4230, 3320, 3695, 4179, 4176, 4204, 4149, 4148, 4114, 4168, 4120, 4160, 3887, 4195], [4208, 4189, 4139, 4202, 4152, 4199, 3504, 4168, 4178, 4141, 2989, 4187, 4151, 3711, 4160, 4148, 4146, 3927, 4143, 4213], [4147, 4153, 3733, 4200, 4141, 4166, 4180, 3472, 4161, 4160, 4174, 4190, 4179, 4131, 4127, 4200, 4183, 4153, 4159, 4195]]
    full_genetic = [[15302, 13978, 15302, 15309, 15070, 16167, 13173, 15319, 13167, 15425, 12697, 15546, 15534, 15614, 13118, 15746, 13498, 13665, 13269, 15452, 13559, 13402, 13935, 13258, 15556, 15276, 13683, 15761, 13515, 12920, 13549, 13290, 13604, 15315, 15270, 15365, 15440, 13197, 13146, 13461, 15642, 12999, 13993, 15490, 15563, 13186, 12929, 13695, 13606, 14846, 13955, 13630, 13868, 14032, 15393, 15325, 15498, 15421, 13406, 13340], [17373, 13842, 17658, 17489, 17463, 17493, 17498, 17502, 17485, 17501, 17534, 17522, 17611, 17501, 17568, 17576, 17369, 17451, 17546, 17453, 17622, 17456, 17508, 17460, 17506, 17557, 17517, 17561, 17530, 17421, 17458, 17483, 17474, 13352, 17478, 17419, 17479, 17554, 17467, 17406, 17475, 17505, 17468, 17495, 17525, 17575, 13382, 17378, 17502, 17553, 17310, 17508, 17663, 17544, 17486, 17414, 17398, 17578, 17448, 17455], [17518, 17481, 17387, 17354, 17463, 17486, 17467, 17507, 17469, 17437, 17514, 17483, 17452, 17426, 17568, 17575, 17558, 17725, 17371, 17499, 17538, 17397, 17548, 17486, 17469, 17509, 17472, 17535, 13883, 17567, 17643, 17437, 17490, 17537, 17495, 17512, 13002, 17540, 17659, 17531, 17519, 17485, 17439, 13271, 17535, 17427, 17561, 17507, 17540, 17523, 17661, 17539, 17484, 17755, 17632, 17507, 17569, 17505, 17511, 17560], [17485, 17423, 17400, 17419, 17400, 17379, 17322, 13226, 17407, 17574, 17482, 17460, 17493, 17490, 17459, 17529, 17393, 17330, 13312, 13847, 17607, 17558, 17497, 17408, 17509, 17498, 17598, 17555, 17408, 17442, 17370, 17415, 17452, 17587, 17472, 17392, 13497, 17464, 17332, 17453, 17538, 17428, 17438, 17431, 17309, 17421, 17533, 17429, 17371, 17434, 17449, 17414, 17393, 17436, 17409, 17318, 17464, 17474, 17490, 17387], [17471, 17504, 17539, 17543, 17481, 17516, 17290, 17503, 17414, 17535, 17499, 17381, 17503, 13937, 17663, 17487, 17726, 17400, 17443, 17409, 17437, 17555, 17507, 17395, 17515, 17488, 17630, 17462, 17725, 17523, 17505, 17480, 17599, 17460, 17577, 17548, 17462, 17518, 17671, 17572, 17516, 17742, 17615, 17437, 17409, 14195, 17356, 17490, 17435, 17608, 17534, 17459, 17525, 17550, 17432, 12485, 17474, 17507, 17500, 17546], [17637, 17658, 17630, 17631, 17680, 17618, 17676, 17633, 17578, 17640, 17628, 17661, 17615, 17651, 17671, 17642, 17648, 17622, 17634, 17573, 17661, 17696, 17673, 17666, 17635, 17609, 17653, 17528, 17640, 17611, 17606, 17656, 17639, 17695, 17670, 17651, 17659, 17624, 17658, 17671, 17609, 17628, 17587, 17661, 17665, 17618, 17641, 17643, 17624, 17637, 17638, 17606, 17634, 13016, 17639, 17630, 17616, 17635, 17655, 17656], [17584, 17666, 17615, 17640, 17610, 17624, 17633, 17643, 17648, 17639, 17644, 17605, 17602, 17665, 17607, 17491, 17549, 17607, 17654, 17651, 17698, 14083, 17677, 17618, 17609, 17627, 17646, 17652, 17661, 17560, 17613, 17624, 17658, 17630, 17606, 17634, 17632, 17639, 17645, 17610, 17616, 17684, 17597, 17685, 17651, 17640, 17643, 17634, 17654, 17619, 17617, 17631, 17608, 17610, 17605, 17648, 17606, 17625, 17656, 17653], [17377, 17431, 17473, 17563, 17500, 17600, 17513, 17464, 17513, 17470, 17426, 17430, 13842, 17391, 17420, 17387, 17413, 17666, 17441, 17421, 17499, 17528, 17469, 17448, 13563, 17483, 17426, 17416, 17241, 17447, 17474, 17396, 17450, 17420, 17414, 12942, 17455, 17451, 17481, 17540, 17525, 17535, 17471, 14384, 17413, 17358, 17419, 17434, 17388, 17447, 17485, 17431, 17389, 17691, 17421, 17514, 17488, 17394, 17379, 17466], [17584, 17594, 17586, 17547, 17577, 17567, 17611, 17580, 17578, 17543, 17580, 17531, 17517, 13774, 17631, 17581, 17568, 17621, 17544, 17588, 17563, 17659, 17565, 17560, 17606, 17554, 17620, 17499, 17546, 17560, 17610, 17591, 17525, 17544, 17636, 17604, 17579, 17651, 17546, 17565, 17587, 17546, 17522, 17553, 17476, 17708, 17667, 13749, 17517, 17579, 17531, 17536, 17592, 17555, 17594, 17559, 17533, 17547, 17652, 17576], [17556, 17810, 17573, 17578, 17591, 17552, 17583, 17617, 17477, 17550, 17580, 17846, 17568, 17580, 17541, 17691, 17522, 17572, 13522, 17618, 17705, 17592, 17566, 17609, 17583, 17541, 17558, 17556, 17652, 17560, 17574, 17572, 17581, 17543, 17640, 12937, 17559, 17571, 17605, 17407, 17602, 17610, 17562, 17691, 17600, 17521, 17604, 17693, 17704, 17546, 17524, 17627, 17631, 17583, 17625, 17716, 17630, 17603, 17649, 17550], [17671, 17563, 17544, 17560, 17577, 17630, 17691, 17548, 17553, 17481, 17563, 17562, 17573, 17485, 17544, 17554, 17547, 17524, 17466, 17551, 17626, 17578, 14112, 17622, 17478, 17576, 17431, 17576, 17574, 17515, 17598, 17581, 17610, 17489, 17434, 13525, 17568, 17541, 17475, 17604, 17576, 17539, 17526, 17572, 17803, 17546, 17532, 17574, 17525, 17534, 17465, 17597, 17548, 17573, 17545, 17563, 17589, 17537, 17541, 17568], [17268, 17320, 17267, 17180, 17395, 13717, 17292, 17299, 17184, 17304, 17329, 17436, 13562, 17465, 17231, 17163, 17252, 17323, 17398, 17247, 17282, 17264, 17357, 17308, 17350, 17308, 17427, 17169, 17319, 14338, 17302, 17270, 17212, 17439, 17418, 17527, 13650, 17127, 17069, 17348, 17467, 17302, 17384, 17341, 17265, 17390, 17269, 17279, 17281, 17255, 17230, 17334, 17375, 17244, 17384, 17241, 13811, 17434, 17269, 13331], [17201, 17240, 17121, 17373, 17202, 13149, 17337, 17445, 17186, 17196, 13867, 17390, 17220, 17247, 17129, 13286, 17270, 17303, 17657, 17346, 17259, 17450, 17305, 17073, 17133, 14101, 17271, 17096, 17141, 17145, 17156, 17352, 17167, 17337, 17218, 13242, 17319, 13380, 17290, 17089, 17268, 17103, 17352, 17322, 17308, 13611, 17205, 17136, 17213, 17232, 17153, 17266, 17174, 17089, 17286, 17497, 13686, 17250, 17314, 17266], [17464, 17412, 17520, 17567, 17491, 17489, 17500, 17564, 17546, 17477, 17521, 17473, 17606, 17503, 17526, 17540, 17511, 17488, 17525, 17531, 17637, 17565, 17573, 17469, 17507, 17557, 17461, 17471, 17600, 17472, 17526, 17495, 17562, 17487, 17460, 17512, 17557, 17477, 17397, 17543, 17544, 17471, 17710, 17582, 17585, 17507, 17464, 17373, 17552, 17656, 13380, 13191, 17689, 17534, 17545, 17511, 17833, 17629, 13666, 17551], [17420, 17512, 17522, 13040, 17483, 17454, 17406, 17448, 17474, 14255, 17528, 17543, 17561, 17370, 17442, 17556, 17289, 17511, 17417, 17502, 17503, 17505, 17395, 17593, 17579, 17478, 17308, 13799, 17520, 17500, 17433, 13308, 17456, 17606, 17560, 17423, 17308, 17533, 17436, 17371, 17538, 17302, 17455, 17434, 17553, 17410, 17366, 17618, 17270, 17468, 17499, 17380, 17479, 17448, 17452, 17423, 17774, 17485, 17479, 17438], [17409, 17388, 17480, 17342, 17507, 17343, 17409, 17498, 17536, 17513, 17420, 17392, 17479, 17499, 17549, 17491, 17536, 17458, 17487, 12865, 17517, 17466, 17512, 17466, 17626, 17463, 17481, 13384, 17465, 17456, 17408, 17464, 17476, 17519, 17376, 13479, 17430, 17467, 17504, 17542, 17363, 17442, 17494, 17468, 17442, 17397, 17483, 13079, 17407, 17496, 17389, 17367, 17425, 17564, 17474, 17492, 17512, 17489, 17493, 17519], [17524, 17681, 17584, 17624, 17560, 12869, 17575, 17578, 17658, 14152, 17567, 17669, 17589, 17604, 17610, 17535, 17577, 17639, 17567, 17596, 17573, 17677, 17544, 17579, 17553, 17575, 17598, 17549, 17615, 17602, 17634, 17631, 17554, 17658, 17576, 17587, 17773, 17571, 17563, 17543, 17577, 17606, 17617, 17514, 17548, 17644, 17580, 17568, 17540, 17573, 17577, 17546, 17655, 17592, 17496, 17673, 17597, 17578, 17568, 17548], [17541, 17474, 17604, 17368, 17390, 17333, 17427, 17438, 17420, 17547, 17467, 17541, 17489, 17365, 17454, 17398, 14040, 17467, 17513, 17511, 17370, 17543, 17398, 13039, 17523, 17394, 17415, 17542, 17406, 17468, 17491, 17456, 17539, 17504, 17446, 17459, 17526, 17419, 17416, 17385, 17517, 17514, 17394, 17405, 17441, 17412, 17424, 13883, 17462, 17446, 13014, 17388, 17472, 17494, 17331, 17427, 17415, 17589, 17434, 17340], [17700, 17700, 17700, 17700, 17700, 17700, 17700, 17700, 17700, 17700, 17700, 17700, 17700, 17700, 17700, 17700, 17700, 17700, 17700, 17700, 17700, 17700, 17700, 17700, 17700, 17700, 17700, 17700, 17700, 17700, 17700, 17700, 17700, 17700, 17700, 17700, 17700, 17700, 17700, 17700, 17700, 17700, 17700, 17700, 17700, 17700, 17700, 17700, 17700, 17700, 17700, 17700, 17700, 17700, 17700, 17700, 17700, 17700, 17700, 17700], [17643, 17634, 17620, 17649, 17557, 17663, 17624, 17627, 17636, 17649, 17599, 17510, 17635, 17678, 17639, 17639, 17657, 17640, 17649, 17638, 17658, 17656, 17649, 17636, 17637, 17612, 17638, 17591, 17615, 17707, 17621, 17556, 17658, 17641, 17663, 17568, 17627, 17641, 17656, 17599, 17635, 17620, 17616, 17660, 17611, 17668, 17641, 17662, 17615, 17632, 17623, 14046, 17630, 17674, 17618, 17636, 17613, 17632, 17689, 17612]]

    mixed = np.array(mixed)
    full_genetic = np.array(full_genetic)

    # Calculate the mean and standard deviation of the mixed strategies
    mixed_mean = np.mean(mixed, axis=1)
    mixed_std = np.std(mixed, axis=1)

    # Calculate the mean and standard deviation of the full genetic strategies
    full_genetic_mean = np.mean(full_genetic, axis=1)
    full_genetic_std = np.std(full_genetic, axis=1)

    # Create a plot
    fig, ax = plt.subplots()

    # Add the data to the plot
    ax.errorbar(range(1, 21), mixed_mean, yerr=mixed_std, fmt='o', label="Mixed Strategies")
    # ax.errorbar(range(1, 21), full_genetic_mean, yerr=full_genetic_std, fmt='o', label="Full Genetic Strategies")

    # Add a title and labels
    ax.set_title("Error bar plot for the experiment with mixed strategies")
    ax.set_xlabel("Iteration step")
    ax.set_ylabel("Score")

    # Add a legend


    # Show the plot
    plt.show()


if __name__ == "__main__":
    main()



