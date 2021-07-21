class PID():
    def __init__(self,goal,x, KPID: list):
        self.sum_now_err = 0
        self.goal = goal
        self.last_x = x
        self.K, self.P, self.I, self.D = KPID
        pass
    def control(self,x) -> float :
        last_err = self.last_x - self.goal
        now_err = x - self.goal
        self.sum_now_err += now_err
        
        u_k = self.K*self.P * (now_err) + \
              self.K*self.I * self.sum_now_err + \
              self.K*self.D * (now_err - last_err )
        print("P",self.K*self.P * (now_err))
        print("I",self.K*self.I * self.sum_now_err)
        print("D",self.K*self.D * (now_err - last_err ))   
        self.last_x = x     
        return u_k

# sum_now_err = 0
# last_x = None
# def PID_control_plus(x:int, goal: int, KPID: list) -> float:
#     global sum_now_err 
#     global last_x

#     last_err = x2 - goal
#     now_err = x3 - goal
#     sum_now_err += now_err
#     KP, KI, KD = KPID
#     u_k = KP * (now_err) + KI * now_err + KD * (now_err - 2 * last_err + last_last_err)
#     print("p==", KP * (now_err - last_err) )
#     print("i==",KI * now_err)
#     print("d==",KD * (now_err - 2 * last_err + last_last_err))
#     print("change_val=",u_k)

#     last_x = x
#     return u_k