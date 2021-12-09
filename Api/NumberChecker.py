#!/usr/bin/env python
# coding: utf-8

# In[102]:


import io
import tensorflow as tf
import numpy as np
from skimage import transform
from PIL import Image
import PIL.ImageOps
import base64


# In[230]:


model = tf.keras.models.load_model('model_2.h5')


# In[231]:


base = '''iVBORw0KGgoAAAANSUhEUgAAAKUAAAC4CAYAAACCYyyfAAAAAXNSR0IArs4c6QAAAARnQU1BAACxjwv8YQUAAAAJcEhZcwAADsMAAA7DAcdvqGQAAAAhdEVYdENyZWF0aW9uIFRpbWUAMjAyMToxMjowOCAyMzoxNToxNTXxrnEAACHsSURBVHhe7d0Hk+u2FYbhtZ3uFCdOnF4mvzQ/M71X1zi9l4c3rwdhtNq90kqiInwzZwCCIAngvDwAKWn3hbu7u3/+26amNqMX/5NOTW1GE8qpzWlCObU5TSinNqcJ5dTmNKGc2pwmlFOb04RyanOaUE5tThPKqc1pQjm1OU0opzanCeXU5jShnNqcJpRTm9OEcmpzmlBObU4TyqnNaUI5tTnN3+hMPUovvPDC3Yc+9KH/bD3bXuuf/3yG0p/+9Kf38odoQjn1X3rppZfuPvjBD/5n65kA+OEPf/juxRdfXAycyj7wgQ8s+//yl78s6R//+Me7f/zjH4vJA/Nvf/vbkpZ/jCaUU+8JkEXDIiFA3/e+99195CMfWfZ/7GMfew9IoMoD7ve///3dX//617vf/va3d3//+9/vfve7370HJpX++c9/Xvbv04RyahG4AFk0fP/737+YckCC0fbHP/7xBdSXX355SR3zhz/8YYHtN7/5zd2vf/3rJSLKv/vuu0sULVLKA/yh6f2lf9s3nmWnbllFxiIgeAAHyI9+9KNL+Sc/+cm7T33qU3evvfbaYp/5zGcWq34SMYENPuXObUoXaeWb0u/ThHJqEYiCS0QEoUioDJyvvPLKYsBkYPziF7+4pI5pfQk+EhXBaRuIgUmALL9LE8qpRaAJRJCBMSBN2UAEpUj5uc99bomUn/3sZ+9effXV5TigiYSmcXlpeRaUTD3A3qezvad0J2rM1DYlOhI/FS0BOcLZ9M3AKP30pz+9mH3WmcDtGLDyeX53Xud/SEdDWSeYuyzTCVZeqpEabp1Sve7QqcuqaZY/+QWUQcR/fMZPTJl0hAx4oy+DfFR1H9LBUNaAGlgjWxiDj5VXXlodDTcAM4JeXqAco2VgApJv5fmc1LVm9MBiijYVS5V7Ejddex2UClrq2feQDobSyTVCgwNUyNZ4kIFOQ7xKyJQxddXR4e6wOjx1GYEQjHxWoOBP+bVv+B6UrRvB6d2j8t5Bju8i5dkI9j4dHSmlLiavU0ATEXVKah8QlVtvfOITn1i27SuyOofOT11OwcVP/MgnUv4RUDzsjApM0c+rH9B5Ya6cjapMfYHsIR0FJQMWIBnYQFgnAtA+ndNJFqwB6Y6UTl1OYCwq8leR03Ypf44CGiDB5hMdYCqT36XO+ZAOhjJpbA0fgQOraCkfoEVKjStSNn1PXVbAGv3ARwKKAMNP+ZmAJ0KCz3FFSuUioZTdp4ei5cFQAhBQGl+k7DUA4HSIARKY7kQdlLZWUU9+6vLij7UC0YzGhykopaAcP6HZFSWLtMHo2H06GEpAluoQuACnA4EqBaYI2TQuVUd9jVWmw51v6vwqAqZg5BP+4aeWWnyV39bH0QhvUs8xRVPH7tPBULo7Akl4B2SmA8xUXWRkRU/7lAdzEE9dVuDhi2z0afv4KzD5n8knddcCIwviXTCPOmpNWYSTAlODx47YNn1LWVCOdZKG7rrLps4ncI1Q8i2/FBWV5Sf7xrqOHWEb80nZrvK1joKyTrQQDkydECVFRPuVNYXblq4BdLyOTm1PfMOHFID8J+UzfpdPY7AZ9Vj/HgylxgWSBo5P3fLAtN10LV+0LIrKt3/qshojmDzjJ/7Jx8oCkH/zsTJ1O4ftffJOdJ8OgtLFxztDXkMCLRg9bWt4r4LAp9yUrtwxOszq0NRlFIT5Iej4SJBRzn98rZ6Un9Wxb58PA7eX547Zp6OmbxoboqEa17st3xyRVyay9o7Sto7a5/g6OnVZjb6Ub7s8PwGTb5spKZ/mz7W8AvJgDE7n2FVn1MFQOnENEfkyUTGzn2mMzjhGNA3UqcspMMaUgUYkG4MHCM1wAZWlPqL0+xwaX5zLt12kHPfv0lGRskZKNRx449TcFB6QlfsGiVcEU5dTU6ogAT6psvxlu1d6/MgCFLAExEDz7SCpMi/QgcfHoiQbYXTMPh0VKTUOkBquwdI6pkN1nMmTxk1dTvzFAMMn/MhvUiDaJ+XP1v9MXcbnwBuhC0z5vrqmrI8h7ZMWiPCwT0evKd1lRUB3GBiZjuhcVkN0fupyMv75DICJf2yDjh8FlowvpU3hji0qgq2vsPW77/KtJUcgbZ/k6TvVQB1ytxXqQSivg/aTgXjoDpk6j8bAMEZAPst3UmWAFGREznydgAYwX8gISADaLr8G0vbJ1pQ61p3FdKK7qo7Z1pERzPHunDq/jD8LTICAMl/yW1AKMM16omcAUxERgFLb5Z2zNHDZY4CkowgJzDoCPo33KkiHdKDywJy6nASFYJTyicgnny+B2XpSUOmhh8k7ZgTTFA08QAaddaV8kIqQ7DFA0lGREnCkMxpdiNdoA2B/nVZn6rLiB/5oTclP4ANbII4Rkf8CkjluPdsBbQTSt88DEKzAfV4dRYrG6SitwZsgbk98Akbg9eBievZOud91M9M1SIGZj0VEoIHM+tGTNQCZaKhchARioB6qJ6UmQMk0MLUdFR35SNTrAQaMX/nKV5bfcCvjN+Utu2w7BmjUWhGEY0pjvvQQnSyUHdOoqadXwDRNgw2EoGT+BEt50NovUo6BZu1T58xETulT6GRQCvdT25FpuOnYuhKYAGzKFiltA7W1JTDHJVhR0hRtDQlEHy2awpWlYwPSyaAc32dNbUMAAxroxvVkQMoXRU3dI5DJQ0xP18G3hvB5nrR36WAox7A+qvJCue0J6DZkXckXrOkbkP5Qlb+eZrsHoF7/rKdvMJYvZWbG3kUe85BDR0XKpoRROq6scp1a15m6nABpzQg+68umb3+kqqnbQw6fqcuf6wAk4AAQfL2LlHoqlx4TJenRUGokCHsiK7yXr+HdjVPbFP8UTPiM70jK8nMqLxL2WmiMiPLsqR5y6EEou1sYALuDhHedUu7Ost0L1rS+w6YuLz5Z+4XfCIB8u8tvHmSsFUVDKUA96DBrzJ6+x2m9qf559SCUGtPdxTRYJ8C57ox6YwTNyH7HTG1P/Mav+c72GFxAmEY4i562GTD7e0Ki6KHR81GRslDfx07BqdzaRDkpGzvXNqszU9sUH/FZBihlNK4RlY/fCPJKyB/d51tlrO9UHqq9UAISYCTiFTF7AVsH6lAA7tKMlNtTPhzFf0VKPhv9CUawAdB/gQhOJkoKPPZnh+rBSEnBpgOtJTVYlBQ5gQtU+eDtmKQjQv3UdpSP1r4i/qXgAp78+vNtUZKJmqZu9Y7Vo6AEnShnmtZ4eRBqOFCDsGipPjjHu3BGyssq/1B+Ir6jtb/st6+yHlqanj1xm7qLlmN6rPZCuQZNXtpHUEXG3mvZN4Z82wFb56fOr8Y/8PhKXnm+k5eOYK41Rk1QElh7JdT+Y58d7m2BxukIG4H0gnUEkgFR59QdoaS2s6nzqvHPlwHIb7YpHwbsPjAJfCAMPmC2bV9R9VDde/Wo14Ggy3wCMK4fdSStwWt7XT51WgWfQCIfnOXJPmVj+X1gBlvA9TbFc4I8PdUzw4NQjuABUWOV6ZDt4NShOq6+lKTqdldOnUciV9AFIfFDsxqfyo/gKufjEcpYAOQIHig97IDSvuodq3uh1LhAAl6d8BrBQw7TmaJnHTMIdSgw13fd1GmVL/IfP8grJ/l8UjBRNvpurDMK7D3MyDMan8iP1V5axjvHw41XQNaUynVavkjJuiulDcDUeWXcgSJyFRSkzW5S4je+onzHp3xdecePAl4AjhE0OF1DeQ9Ch+jBEFbDNJaBtK832a6jOiS1n1p7TJ1Xxh1UoCP+k+cr+cy2QJMf8x1/Voc6bpRp27tJURGAgAzSImXAHqIHoRxVZzSeAdHUXaPHVCdrWA2u8WncP/U0MvYZ6Cyz+Axs8vxlhrOtnCmrTj7MJ3zGdk3LouH4rfMgzf+Hai+UTj5CqFOiZNO4TlevzqTCtwZbg2h8H9j3KqHPSNlTrEVuXcEgUvKNlK+8LfGfZ6X9BkeEZEVRQOaXBEYPNsHGl8rWCuB0rD8fjJSiIRgL8zRCqEyd1iE0NlKn2pZmrUvSmJ86TAIHPwCzZ4B+5iAd8/zJb44pQtpO/MN3lgPMdl9RA2/+Kl378xg9ak0ZgEknmE6UgnNdT0NJY3Vw7OSx3ySZ+l8ZT1DmHwAKKMHIzHA9oDIA8xs41xIVg43PKhMF820ag8+xeu41pU7ojHWIfHeXThVJKRB1wlTOdMZU3uek6owdnjpO+YBPgo6NkVL0VCZS5j8gj1DyjWhYIGH8N4KpLAFUWRr3HaK9UOpgjQ3I7qyM1kCmgNsV7ilQW39OHa8xcJjCA3IEU/SsDgOm49ZgjnDyY1DyIRCDb/QvxcWhehDKYGtKCEad0onK1HPHreEs/Gu49QgzdfdNkxkln0b5BWB8wy/Spm2/WpQ2ffegymdFynzHXwEZlMoYvxG/MvvHKKmO8mO0F0qqsxotJXeazpvCpYx0qjp1hDRSRFSWre+uqYcFNGPca7giHVPG1Okhp/Vkv+v2O29mn7qtP0cgAZaP+IwVRAQUQaRPdNSxHZTNeCeHcpfqQBAG4igN1Uipjq3vpixVf+qZjC24RnPzi3bWg6+++uqSMmV+u/35z3/+7gtf+MKy774ICUjnAmWzHTj5oilawAhG3zB/9913l5flIPRKLzDXPgS4447VQVDSLhDX0mB3F+B0pM71uw7p2Kkxf6sCDCBFP2PM0b2Sa4YCFsDA5m8AeQcJPgbIcQ0JuCJkU7ZzuEbBhZq5pIArOvITAyezP5+uVfDR9mN0MJT3SceCq9Qd1hO30D7uV6bzld2ixmmZYwMSPKJZ+8DIAq6UAXMNp9S+MUK6FnO+omVqmdVUHZCCCRgLJPwpP0ZLxzmvdje9H6onh5K664KuO8j0XPi3TTpfvVsUJ3IySQNS2gNLr29EyqbigAReQJq+v/zlLy9/2o/5qxfKA9I5MxF0jJR8wC/aAEp+CkgR8p133ln2gTKf2c7ys/JjdRIoU2tEDZVn7kadNgDKM9u3KNHQug50IheBEjBFShCZfu0HpDJA+vs/IqL1ZGtKINqnvjJAgnlcR5Y2jRMfCCZ8BDowBuTbb7+9QGk7CNULYtJm/XgKnQRKHSzVaCAGpLupzt8qiDQ6ERi2SVoUA08WmD3YMNABEIgADU7brSGlwGxNykRf13B91rX5JeBEyhHI1pSsoJIcI1KOkfcYnSxS6iCNEVFZHQ/QAN6KOCsniSTMtrT12LFWtCpiAa59rhM4ohuYinY9qAANjMpM34Bkyse1pP3qS53H9bqGtL4y/gBWUPIN+EzhI4zWi2OUdFyy/RQ6GZQ5dpcaiFPJuQ180+LzGGdxYA8H6/xjTSQDCBO5imaelkWzL33pS8vrG2bdp+y11167++pXv7pMw0y5sqJgUzXgmOtomzaPpv/6DrpRRbL1+AsM4BpnNgY8cAZpQSQg2SmeBbRsZ6jSKR03KFKDZ3Dkv/a1r7234B7XLO5UqWgo5P/kJz+5+9nPfnb35ptvLvlf/epXd7/85S//a3rQeXl27FMbActgiQoG8DFTir6CmDjVQDvP6Dh1GK2dvUuu27VFwvLOIW+c1nI9566+NshL9UeZ8XYO7XQOaRGXKdMXvpHadg5WH+uX8wSo9eIbb7yx+On1119f/PSLX/zi7uc///ndW2+9tQCpDn9JPfDw2TiNP5VODqVO1dk1lDokrYNPAWUO48DyD4lT1OM0x3HyCF6wsJYb8s6/T0ConnMYp4AEvnPtap9j1HVMYDrOtug45qW2nSd41zCWD0r1O0cCGl/xDz8BMij5zzTuZucn6dVC+dOf/nRZKAMyKHU0KHVU3aeC0sAbaKb9nDQOPNlWz51vvwGuHodyrnzOp84lSqiT1udey3WcLxiNl2OU1VYqBWl5YBpL28z1QdV+kte2bhZ1nNf1lMuzNZTUedQjvjCrgZLf+Mm2qMmHZjU3kpSfAvRqodRBQOpkT3JS9QzGU0FpoF0fAJxAAGD7ZD/YOj7n609S1jkpp0r1X9udg5Oq1z7HOpd2GS/bgdS1Rtl2rpYh6/3a6KGDitxJXfvzibawxoX4lrXtHGsoRUjpj370oyVS5itgurbtq4VSqoOglAYlM+g6ynSwhfShauClnMPhokeDv0v6yWnqSNUXJZXrH3WuYCP1AQMuTjIGaylzPmPEOmd117Cpy8muZQydGwTSZHxYY6WeG6Jx0ybnd4y8sdBueddnXVdqm/jgxz/+8XtrSjD+4Ac/WAKKwCJwmCm8w5S6Pv+dAkot+saz7H8rJ+mgNPjkAamTBpGJNAZSmdQAGaiin45wnFQnTN/Or3O2dU6eAwyUfYeYthhkqXZwiLx2Fw2lOakyDqxf6uqrY91kjYGb0blysm3HgQzEyp3LPmbbvp68lbmpva6xbV83tnM5h+s2tlLHKHNdZVJt1lep8WIETvkg03/tY/LM2AZvQDrG+UAGzN5LygscoqRUPT5yHWn+kj61DoLSAEoNko4ZoBxc58EYgKVkUOyn6jZ4HKnMeZ7XtG+ESVuLSrXbPu0d2y+vPjAc7ximbmDIM9fpWHn1nEOflOmLcdAX13RM166NyvRRO4xxcmzOJg4HQDesvHEED3ODN7uUuvEd5/rOVz6ISblrS7W7PP8EIjCLjh6AnFc7XMM51XVsN8JT66Dp2/sy79sadIPNgcGgk14jMHedtClbZxtE4Op0eanOdzc/Vq7XTSEPAo5XFiy2u7s7RpmBdRyzHTSOlVcvJztXN1XH2qfNayk3hs4hBTOAO79z1JaxXc7pGsx5bVcOSvUAKTVe3fTBHPzaKirzC590fYBm2tCNAcAf/vCHyxRu6v7+97+/LL9se6XnWtrkWtrl+uN1n1IHQ2kK0lGdDkrbzLHuOsCNd5wykBpIYBpoZTrcAB8jg84pBlq+CAWCfdJe9YAU3I7Pac7DCfav5dxBqQ4nOU4a3M4hdU7nCAh1MmOhHdLGQd7NSoCQD0551wtK5aStggO/8Zdozjds7JNrjVDyw/e+973lYQeIoLSmZHyojQFJF4FSg3XEJwtSHZQHZHegzus0UOVFAducIeQDEZBNNU0FAShfx9QzsDrr2ruizz4ZcAPt2tphsANzDZNy11XXNQHj2OAJJPUIEMpGdax9JNUv7afOP15bXt9I/RFIx3UO28rLGwvn63qANH7yxrD6to0///i2EL/4BIhv+M1YjFAGpHaJhiKkBx1ASgEpenoidw1GpwSS7oVSg+sUAHXUlC1CPgZKg9YDjkFsIJVJDbiOdceXN7CUcx8rg9zSAUBFSKltA++68pwcVI4j2zmsiGJfZbVHmTY6n/Mod14KMH1R7liW9Nm5O8Z51HWeETD7jZO8fY4LUqkbXJ2OV26bwCeA+OpayyxRk98aH9LfEUpvR0RI0TIYSy2/ArC2d71TaG+kBJhpG3T7oGTyPSgAwYAaLCYPOAOsQ+UNausjDtnVUXVIe+Qb1LE8BWaR0mCv13CdJ9A6Xqq+c+Ss1DFjvlR/OCxHrWEj2/qsnuOktkmqrjpmC/ucp5nDfmOoTqCqo75tqfpdq2UWKH2ODsw+Z7e0cn2SNi5BKVJ+5zvfWUBs+lZmycU/rkWud0rdCyXngLF1ZFDqJAPlCOMIKCgbXIM5OsugMuXqdJdL6/ShMj0BCogikj4oM/hPpdqfardUf/QLIEyZtBuOBZYy+zu+cvmAVNZNHLzKXIcav8bNLGCJZXYzfX/9619f4JRXbixahgBRe6Rk3XgflN5V1rZzaO8rIc7kXNEHaJzszgKezuWcotKYBp2OdDdKy1fXtus4vzLnPcS006C7QWw3becI19J+aWZ7NG1t4EcHdFPprz7Ztl8ZKEr1GTzqtd2UbMq1zwMFsKyvA9a28kAtL3Vcpl6gMsdrR9fTLmPJPwKJwNGM1rjoZ31q/Mn1ejsi7UMOEdQ1x/E4tfZGSjAWDVs3iph1ej2N9xTe9KkjBo50vo5VbmByuLIcTurbNnDqGlBONujKnZ/UDyrHFCFLwekY53e81DHjdpJfl0tdLwDar0zeuTiUwAG86jAOrV8ga18QSZ3bcV1DpLSvcnUC37lG6XNmjEzTpm2fuomYIuWu6XuU8fGgYz1pXTlGym9961vLPu05l+6FkkQZ8AWbbWtKDrdtX7CqE5hgDppgsd3gNfg0OphT1ZM+JOelnMQhzq28iCAtIjonC4pA4eikXWPbyHZ11AdH7ZM6V9vOCdAcWNRkyru28415sq2O6zle3vm6/nidpF/Giz+kgkHTNzADUpllmP27oHRt4AGyKZsB89vf/va2oNRZkIHRXQY6TgZkBkidBWLb6gWhfckdyQzu6HwDTjquzGBziOOdZ5caJPW7FgWndgYkOZ/rSF0fXLalzqWctCsYCBD2267dUmX2GaMiIFXHOTpnEDrGNFxd9ewbrz0e3z5lTN6x+qWPxry+mhH4ynrfGpKB0xeFgekJXFu7duqcQfnNb35zSXtx/t3vfndbUAIIkEzeIHByIIqSAFRe1ARmULIGTr4IRgZ5dI5ykOi8QbYv0O6TOga1a2mjY3JU11UviNQHhrSpdYx+tUGZ44J2nF6dpxtprD8qkDomq57rtl+e7DNG2kfVkbqGvNTYA4yBkeUn8HkgZaBsW6RUv3N1fte37bWPd5MgbOr2flK6KSgDicnrtFTn5AEYiMwa03YDpG5QAsZxa9A4ymCDUpps23ffYDg3jfuDkuxv2+CDp+mU0+VB0JSpnAWJfUHEHN8UDMpgU+466ijTbmmSH9vomK4hT/LJ+bTZMY2H/W07vzEVFeUFAGNdpASf9WPTuG15yy43qnN1PW12Xu3xUANG0TEo5YHq4Wfsw6m1F0riXFBqFKiCwQCImCOYpZxksAxag+dYZt99ykmJc9Zlade+gCR51yVO4IBetUg5QXllRVFQSDkKhPqtrAcO+aCUrw1SdTleGlBrqRcUtVeZcxkb1zHG9jHXSY4Dn6WUcQWn7db0+UB0DER5JmA4fzeE9jFt1R/g9f1JQGbKjJV659KDUFKD10CRDur0GswRSoNrP0c15QD83OIIUJquexUj5RRR0zYYqMgJlNaKnOhY4JQWGddqfBz3POJ0x+b8xnoNgxutNyDGVgpI42vs+7GZOvLqiJZ8xR/arj9SMAal8fD0DUKffwel/Cah3CWg6axBccc2KMy+oDRgUjCq02DT8zqODj02mAKRE4LNgIOs6awnX3mmDgCLlDlUnXOradr4GuuCQcGhDzcAaR8Ye3Vn7Go7Mxb6rL9uQFO1SAlMX8i+OigBBr4GyKA0tYiUUjC6s1tXAlOdS6gI2ENO07btABcti5JMHan6nCjPqQF6CSitH3sTEpBjCkBrSimfBKW89neD6Yf+GhdlwOsXAmDsNzpXBSXgDE7rGoNleh5hVQeMwCxKkroGRUcdDwx1QJvznRM0jFzL4Nnn/Oo7h2tWrzpF5qbkZB+QnEOklNrmGHlGRUrb2ug88q7hmky++ueUsTO2IOubQIBk4Csq2m8aNybKHNPNpX+ZMWmNbV0pWgITlCC9OigB1TqRGTBRMhDtT8qBFpgc6hx1tvx6v1TZQ/Xa77pFsI4n+8FlHwtwJnKYxqpL8kHtWMeAUblt+a55TgWl1zxFRlZeCkZpQPJDUOqTvpuuwcj0xesfr378PgeQtsFp+2qgBAUQRa2mZIDats/gSRk4gsgxgeE4MFQu3/FAcb5Sg6l8rEciVvUMnOuq65rqBJ56rqm8KTvAlHeuypN8wKqrDruU9E8ktGYEXC/I5a0lgxGETfG2gandIAQkMI2DPPNZt6goWgakd5dANatcBZSpaZdEQ9sBSIG0BQEXqCIDAQ2QI4i2tTlQE6c4/tICJRBBCEZ560YPnUy5OiAEb6kb180FSpAVKcuDMRD7rTc4peC9KihpjITy1yIgFvXcTEVD4Abr1hSUoqLPt0HonaQpG3w9dIqO1vG2Rc1mGBD2DaCiZOtJELbPrxibus8N5ZMQpMGcyESTa7FxGtb2Bl75FoHcpZYp98nNNkof9d1sAdKmbvBZ9ngQKl3PFufS9YS1qXtllhqXTPcJkGAEmxR4wMyUZZcCkiaUNyTRH2wBKGKamjMPP6Jks4RUvXNO3TShvBEBq+WKPPg86ADT1C1vPwgD1Pa5gaQJ5Y2ptbQoCDgwBqyHIDDaZiLqhHLqpGpaBltTNxiB6YEHgMrXU/i5NaG8IVlPFiWBJ980XT4w2aU0obxxAVTE9Dk4ID2RX1oTyqlF4BynaoBeYj1JE8qpzWlCObVTPim61EfGE8qpzWlCObVTnsbnZ99Tm5Iveay/zHEuTSin3vtCx2O/2HFqTShvSGv4mGjoO5e+fynv+5rtu5QmlDck0DUl+ymKvC8CU4CSqXvfdzRPrQnljWiMfOAbX/f4GYttoErtn5Fy6qQC2AhhDzF+IhGM8kVLkF5SE8obUWCOUdKPyQBpn7zyfiJ9SU0ob0RBmaUgVOYhZ4ySTevn1oTyRtXUDUgPO4AcH27kLxU1J5Q3qoCk1pgjgPb7VOcS3xSaUN6oHhMB5/Q9tTn59vmMlFMnkS/vHvLlCtP6jJRTmxKQx2+jn0sTyqn/kejIZqSc2ow8BF0CxjShvEH1VO1TnPFbQcrGF+iPeUI/hSaUN6Y+2wagNDC9QPeRo22mHqlzbjgnlDekQARZn3XLK2PjJzqpOufUhPKGBK6sqdqXe/uS7/jPEs4N4qgJ5Q1KVOzbQtJMpPRXf/0lYKl6l9CE8sYEPFaULFKyQKUZKacuqqZzgPb9yktqQnlDAlsAlh+1q+wSmlDekAJynKa3qAnljekSn2U/ryaUN6ItR8a1JpQ3oNaKouSl/ubk82hCObU5TSj/DyQCXsNa8bGaUF6pAtGPu/xR/VEjpP4TxLUBO6G8QgVZ/wMHeP4Hju3+exhQWz+q71vkHnZ2felia5pQXqH6PzegC0AR0w+9+mOn9vfPmfwXMZK/1B9CfR5NKK9U4CPwgRGc/g+Ofz3CAnScvkXKa3g1NKG8UomOImAGvsx2+0eBM0C3rAnlFSq4gMf8QyYmQtoOzGsAcJcmlFem/j1dwFkjNmVnpm1QAlVqW31rytaV0jW0trNLakJ5ZfJlCpGQiozAk/cEPsLpn4C2zpSqK9+/vSvSBqyyzn1J+XXQN55lp65BAOpbPl7vyANKOu7ro0VREWjg88ro7bffvnvrrbcWAypw33jjjSX/+uuvL//7WxkL0nMvBSaUV6Z+8NWPvQAZfCA1vRc9A0oKOvAxQILuzTffXKLmO++8s5QD0rZjnMP0D+Se9M8l3+i8ztXwDcsPvF5++eUlKsqD088bGGh9g/yVV15Zfmujjrzf3FAPRSDtVRKgi46AtAxg9rEJ5dSDAh/Y/HQBkEAULW2DLzDtC96gFDUDE2yA7JMhKVBN2+AEJHjVOacmlFcokAHOdA1AKg9O0AakbX+1VxmBDnBAA6JpWgpQMEoDtqnf/nNqQnmFAhm4pNSDDTBZIPbpTUAmDy2BmcCnXJl9tK5zLk0o/w8UlCSKHiNRsSftSwBJE8qpzWm+PJ/anCaUU5vThHJqc5pQTm1OE8qpzWlCObU5TSinNqcJ5dTmNKGc2pwmlFMb093dvwCnS6tdunGDXQAAAABJRU5ErkJggg=='''


# In[232]:


imgdata = base64.b64decode(base)
stream = io.BytesIO(imgdata)


# In[233]:


def load(filename):
    np_image = Image.open(filename)
    np_image = np.array(np_image).astype('float32')/255
    np_image = transform.resize(np_image, (28, 28, 1))
    np_image = np.expand_dims(np_image, axis=0)
    return np_image


# In[234]:


img = load(stream)


# In[224]:


#img = load('./cbimage.png')


# In[235]:


result = model.predict(img)
predict_classes = np.argmax(result ,axis=1)


# In[236]:


print(predict_classes)


# In[ ]:




