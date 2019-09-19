@@ -0,0 +1,303 @@
import functools

class Relation(object):
    def __init__(self, sets, rel):
        #relΪsets�ϵĶ�Ԫ��ϵ
        assert not(len(sets)==0 and len(rel) > 0) #������setsΪ�ն�rel��Ϊ��
        assert sets.issuperset(set([x[0] for x in rel]) | set([x[1] for x in rel])) #������rel�г��ַ�sets�е�Ԫ��
        self.rel = rel
        self.sets = sets

    def diagonalRelation(self):
        #���ش���IA��Relation����
        #��ɾ��pass����ʵ�ָ÷�������
        R = frozenset([(x,x) for x in list(self.sets)])
        return Relation(self.sets,R)

    def __mul__(self, other):
        assert self.sets == other.sets
        #ʵ��������ϵ�ĺϳɣ���self*other��ʾother�ϳ�self����ע�����ȿ�other����ż
        #���غϳɵĽ����Ϊһ��Relation����
        # ��ɾ��pass����ʵ�ָ÷�������
        A = self.sets
        R1,R2 = self.rel , other.rel
        R = set([(x[0],y[1]) for x in R2 for y in R1 if x[1]==y[0]])
        return Relation(A,R)

    def __pow__(self, power, modulo=None):
        # ʵ��ͬһ��ϵ�Ķ�κϳɣ�����**���������self*self*self=self**3
        # ��ÿ����֧�з��ض�Ӧ�Ľ���������һ��Relation����
        # ��ɾ��pass����ʵ�ָ÷�������
        A = self.sets
        R0 = self.rel
        if power == -1:
            R = set([(x[1],x[0]) for x in R0])
            return Relation(A,R)
        elif power == 0:
            return self.diagonalRelation()
        else:
            t = Relation(A,R0)
            for i in range(power-1):
                t = self*t
            return t

    def __add__(self, other):
        assert self.sets == other.sets
        #ʵ��������ϵ�Ĳ����㣬����+���������self+other��ʾself��other
        #��ע�⣬��Relation����rel��Ա�Ĳ�
        #���ؽ��Ϊһ��Relation����
        # ��ɾ��pass����ʵ�ָ÷�������
        return Relation(self.sets,self.rel | other.rel)

    def __str__(self):
        relstr = '{}'
        setstr = '{}'
        if len(self.rel) > 0:
            relstr = str(self.rel)
        if len(self.sets) > 0:
            setstr = str(self.sets)
        return 'Relation: ' + relstr + ' on Set: ' + setstr

    def __eq__(self, other):
        #�ж�����Relation�����Ƿ���ȣ���ϵ�����϶�Ҫ���

        return self.sets == other.sets and self.rel == other.rel

    def toMatrix(self):
        #����ż������ʽ�Ĺ�ϵת��Ϊ����
        #Ϊ��֤�����Ψһ�ԣ����self.sets�е�Ԫ��������
        matrix = []
        elems = sorted(list(self.sets))
        line = [0]*len(self.sets)
        for elem in elems:
            #���ڴ˴���д����ʵ��ת��Ϊ����Ĺ���
            for i in range(len(elems)):
                if (elem,elems[i]) in self.rel:
                    line[i] = 1
            matrix.append(line)
            line = [0]*len(self.sets)
            #���������д���򣬲�Ҫ�޸�����Ĵ���
        return matrix

    def isReflexive(self):
        #�ж�self�Ƿ�Ϊ�Է���ϵ�����򷵻�True�����򷵻�False
        # ��ɾ��pass����ʵ�ָ÷�������
        for a in self.sets:
            if (a,a) not in self.rel:
                return False
        return True


    def isIrreflexive(self):
        # �ж�self�Ƿ�Ϊ���Է���ϵ�����򷵻�True�����򷵻�False
        # ��ɾ��pass����ʵ�ָ÷�������
        for a in self.sets:
            if (a,a) in self.rel:
                return False
        return True

    def isSymmetric(self):
        # �ж�self�Ƿ�Ϊ�Գƹ�ϵ�����򷵻�True�����򷵻�False
        # ��ɾ��pass����ʵ�ָ÷�������
        for x in self.rel:
            if x[::-1] not in self.rel:
                return False
        return True

    def isAsymmetric(self):
        # �ж�self�Ƿ�Ϊ�ǶԳƹ�ϵ�����򷵻�True�����򷵻�False
        # ��ɾ��pass����ʵ�ָ÷�������
        for x in self.rel:
            flag = x in self.rel and x[::-1] in self.rel
            if flag:
                return False
        return True
                

    def isAntiSymmetric(self):
        # �ж�self�Ƿ�Ϊ���Գƹ�ϵ�����򷵻�True�����򷵻�False
        # ��ɾ��pass����ʵ�ָ÷�������
        for x in self.rel:
            flag = x in self.rel and x[::-1] in self.rel and x[0]!=x[1]
            if flag:
                return False
        return True

    def isTransitive(self):
        # �ж�self�Ƿ�Ϊ���ݹ�ϵ�����򷵻�True�����򷵻�False
        # ��ɾ��pass����ʵ�ָ÷�������
        for x in self.rel:
            for y in self.rel:
                if x==y:
                    continue
                if x[1]==y[0] and (x[0],y[1]) not in self.rel:
                    return False
        return True

    def reflexiveClosure(self):
        #��self���Է��հ���ע��ʹ��ǰ���Ѿ����ع��������
        #����һ��Relation����Ϊself���Է��հ�
        # ��ɾ��pass����ʵ�ָ÷�������
        return self+self.diagonalRelation()

    def symmetricClosure(self):
        # ��self�ĶԳƱհ���ע��ʹ��ǰ���Ѿ����ع��������
        # ����һ��Relation����Ϊself�ĶԳƱհ�
        # ��ɾ��pass����ʵ�ָ÷�������
        return self+self**-1

    def transitiveClosure(self):
        closure = self
        while True:
            if closure == closure + self*closure:
                break
            closure = closure + self*closure
        return closure

    def transitiveClosure2(self):
        closure = self
        # ��self�Ĵ��ݱհ���ע��ʹ��ǰ���Ѿ����ع��������
        # �÷���ʵ�ֵ��㷨���ϸ��մ��ݱհ����㹫ʽ�󴫵ݱհ�
        # ��ɾ��pass����ʵ�ָ÷�������
        for i in range(1,len(self.sets)):
            closure = closure + self**i
        # ���������д���򣬲�Ҫ�޸��������
        return closure

    def transitiveClosure3(self):
        #�÷�������Roy-Warshall���㴫�ݱհ�
        #�ֽ���ϵת��Ϊ�����ٵ���__warshall����
        m = self.toMatrix()
        return self.__warshall(m)

    def __warshall(self, a):
        assert (len(row) == len(a) for row in a)
        n = len(a)
        #����������ʵ��Roy-Warshall�󴫵ݱհ����㷨
        #����a��Ϊһ����ϵ����
        # ��ɾ��pass����ʵ�ָ÷�������
        for k in range(n):
            for i in range(n):
                for j in range(n):
                    a[i][j] = a[i][j] or (a[i][k] and a[k][j])
        # ���������д���򣬲�Ҫ�޸��������
        return a

def isEquivalenceRelation (rel):
    #�ú����Ը�����Relation����rel���ж����Ƿ�Ϊ�ȼ۹�ϵ
    if rel.isReflexive() and rel.isSymmetric() and rel.isTransitive():
        return True
    else:
        return False

def createPartition(rel):
    #�Ը�����Relation����rel�����������rel.sets�ϵĻ���
    #���rel���ǵȼ۹�ϵ�����ؿռ�
    if not isEquivalenceRelation(rel):
        print("The given relation is not an Equivalence Relation")
        return set([])
    #��rel�ǵȼ۹�ϵ������ʵ���󻮷ֵĳ���
    partition = set([])
    # ��ɾ��pass����ʵ�ָ÷�������
    for a in rel.sets:
        t = [x[1] for x in rel.rel if x[0]==a]
        partition.add(frozenset(t))
    # ���������д���򣬲�Ҫ�޸��������
    return partition

def createEquivalenceRelation(partition, A):
    #�Ը����ļ���A���Լ�A�ϵ�һ������partition
    #�����ɸû��־����ĵȼ۹�ϵ
    assert functools.reduce(lambda x, y: x.union(y), partition) == A
    return Relation(A, set([(a,b) for p in partition for a in p for b in p]))

def isPartialOrder(rel):
    # �ú����Ը�����Relation����rel���ж����Ƿ�Ϊ�����ϵ
    if rel.isReflexive() and rel.isAntiSymmetric and rel.isTransitive():
        return True
    else:
        return False

def isQuasiOrder (rel):
    # �ú����Ը�����Relation����rel���ж����Ƿ�Ϊ��۹�ϵ
    if rel.isIrreflexive() and rel.isTransitive():
        return True
    else:
        return False
    
def isLinearOrder(rel):
    # �ú����Ը�����Relation����rel���ж����Ƿ�Ϊȫ���ϵ 
    #���򷵻�True�����򷵻�False
    if not isPartialOrder(rel):
        return False
    else:
        # ��ɾ��pass����ʵ�ָ÷�������
        for x in rel.sets:
            for y in rel.sets:
                if not ((x,y) in rel.rel and (y,x) in rel.rel):
                    return False
        return True


def join(rel1, rel2):
    #�Ը����Ĺ�ϵrel1��rel2
    assert rel1.sets == rel2.sets
    #���ȵõ����ߵľ���
    M1 = rel1.toMatrix()
    M2 = rel2.toMatrix()

    m = len(M1)
    n = m
    M = []
    line = [0]*n
    # ���ڴ˴���д���룬ʵ�ֹ�ϵ�����join���㣬�������M��
    for i in range(n):
        for j in range(n):
            line[j] = int(M1[i][j]+M2[i][j]>=1)
        M.append(line)
        line = [0]*n
    # ���������д���룬ʵ�ֹ�ϵ�����join����
    return M

def meet(rel1, rel2):
    # �Ը����Ĺ�ϵrel1��rel2
    assert rel1.sets == rel2.sets

    # ���ȵõ����ߵľ���
    M1 = rel1.toMatrix()
    M2 = rel2.toMatrix()

    m = len(M1)
    n = m
    M = []
    line = [0]*n
    # ���ڴ˴���д���룬ʵ�ֹ�ϵ�����meet���㣬�������M��
    for i in range(n):
        for j in range(n):
            line[j] = int(M1[i][j]+M2[i][j]==2)
        M.append(line)
        line = [0]*n
    # ���������д���룬ʵ�ֹ�ϵ�����meet����
    return M

def booleanProduct(rel1, rel2):
    # �Ը����Ĺ�ϵrel1��rel2
    assert rel1.sets == rel2.sets

    # ���ȵõ����ߵľ���
    M1 = rel1.toMatrix()
    M2 = rel2.toMatrix()

    m = len(M1)
    n = m
    line = [0]*n
    M = []
    # ���ڴ˴���д���룬ʵ�ֹ�ϵ����Ĳ����˻����㣬�������M��
    for i in range(n):
        for j in range(n):
            t = [M2[k][j] and M1[i][k] for k in range(n)]
            line[j] = int(any(t))
        M.append(line)
        line = [0]*n
    # ���������д���룬ʵ�ֹ�ϵ����Ĳ����˻�����
    return M