from openmdao.api import ExecComp, IndepVarComp, Group, NLGaussSeidel, \
    ScipyGMRES, Problem, ScipyOptimizer


class PMAD(Group):
    """ Group containing the Sellar MDA. This version uses the disciplines
    with derivatives."""

    def __init__(self):
        super(PMAD, self).__init__()

        self.add('InputVoltage', IndepVarComp('Voltage', 500.0))

        self.add('Motor', Motor())
        self.add('Cable', PowerCable())
        self.add('Inverter', Inverter())

        # shoudn't the inverter's input be the powercable's output? PowerCable calculates
        # DC transmission losses, and Inverter is outputting AC to motor, motor itself does
        # not connect to cable comp, signalling that the PowerCable supplies the Inverter,
        # in which case the loss after transmission accross the cable i.e. the OutputVoltage
        # should be connected to the Inverter's InputVoltage
        self.connect('Inverter.InputVoltage', 'PowerCable.InputVoltage')
        self.connect('Inverter.InputCurrent', 'PowerCable.Current')


        # what about power connection?
        self.connect('Motor.InputFrequency', 'Inverter.OutputFrequency')
        self.connect('Motor.InputVoltage', 'Inverter.OutputVoltage')
        self.connect('Motor.InputCurrent', 'Inverter.OutputCurrent')

        self.nl_solver = NLGaussSeidel()
        self.nl_solver.options['atol'] = 1.0e-12

        self.ln_solver = ScipyGMRES()

if __name__ == '__main__':

top = Problem()
top.root = PMAD()

top.driver = ScipyOptimizer()
top.driver.options['optimizer'] = 'SLSQP'
top.driver.options['tol'] = 1.0e-8

top.driver.add_desvar('InputVoltage.Voltage', lower=0.0, upper=1000.0)

top.setup()

# Setting initial values for design variables
top['InputVoltage.Voltage'] = 200.0

top.run()