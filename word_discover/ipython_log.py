# IPython log file


get_ipython().run_line_magic('cd', '~/code')
get_ipython().run_line_magic('cd', 'word_discover/')
get_ipython().run_line_magic('ls', '')
get_ipython().run_line_magic('run', 'discover.py')
ngrams
get_ipython().run_line_magic('ls', '')
type(ngrams)
ngrams
ngrams.iteritems
ngrams.keys()
ngrams.items()
get_ipython().run_line_magic('load', 'discover.py')
# %load discover.py
#================================================================
#   Copyright (C) 2019 UltraPower Ltd. All rights reserved.
#   file: discover.py
#   mail: qinhaining@ultrapower.com.cn
#   date: 2019-05-13
#   describe:
#================================================================

from collections import defaultdict
import numpy as np


def gen():
    lines = open('/home/siy/data/广电全量地址_weak.csv','r').readlines()
    for line in lines:
        yield line
texts = gen

n = 4
min_count = 128
ngrams = defaultdict(int)

for t in texts():
    for i in range(len(t)):
        for j in range(1, n+1):
            if i+j <= len(t):
                ngrams[t[i:i+j]] += 1

ngrams = {i:j for i,j in ngrams.iteritems() if j >= min_count}
total = 1.*sum([j for i,j in ngrams.iteritems() if len(i) == 1])

n0 = 5
min_proba = {2:n0, 3:n0**2, 4:n0**3}

def is_keep(s, min_proba):
    if len(s) >= 2:
        score = min([total*ngrams[s]/(ngrams[s[:i+1]]*ngrams[s[i+1:]]) for i in range(len(s)-1)])
        if score > min_proba[len(s)]:
            return True
    else:
        return False

ngrams_ = set(i for i,j in ngrams.items() if is_keep(i, min_proba))


def cut(s):
    r = np.array([0]*(len(s)-1))
    for i in range(len(s)-1):
        for j in range(2, n+1):
            if s[i:i+j] in ngrams_:
                r[i:i+j-1] += 1
    w = [s[0]]
    for i in range(1, len(s)):
        if r[i-1] > 0:
            w[-1] += s[i]
        else:
            w.append(s[i])
    return w

words = defaultdict(int)
for t in texts():
    for i in cut(t):
        words[i] += 1

words = {i:j for i,j in words.iteritems() if j >= min_count}


def is_real(s):
    if len(s) >= 3:
        for i in range(3, n+1):
            for j in range(len(s)-i+1):
                if s[j:j+i] not in ngrams_:
                    return False
        return True
    else:
        return True

w = {i:j for i,j in words.iteritems() if is_real(i)}


# %load discover.py
#================================================================
#   Copyright (C) 2019 UltraPower Ltd. All rights reserved.
#   file: discover.py
#   mail: qinhaining@ultrapower.com.cn
#   date: 2019-05-13
#   describe:
#================================================================

from collections import defaultdict
import numpy as np


def gen():
    lines = open('/home/siy/data/广电全量地址_weak.csv','r').readlines()
    for line in lines:
        yield line
texts = gen

n = 4
min_count = 128
ngrams = defaultdict(int)

for t in texts():
    for i in range(len(t)):
        for j in range(1, n+1):
            if i+j <= len(t):
                ngrams[t[i:i+j]] += 1

ngrams = {i:j for i,j in ngrams.iteritems() if j >= min_count}
total = 1.*sum([j for i,j in ngrams.iteritems() if len(i) == 1])

n0 = 5
min_proba = {2:n0, 3:n0**2, 4:n0**3}

def is_keep(s, min_proba):
    if len(s) >= 2:
        score = min([total*ngrams[s]/(ngrams[s[:i+1]]*ngrams[s[i+1:]]) for i in range(len(s)-1)])
        if score > min_proba[len(s)]:
            return True
    else:
        return False

ngrams_ = set(i for i,j in ngrams.items() if is_keep(i, min_proba))


def cut(s):
    r = np.array([0]*(len(s)-1))
    for i in range(len(s)-1):
        for j in range(2, n+1):
            if s[i:i+j] in ngrams_:
                r[i:i+j-1] += 1
    w = [s[0]]
    for i in range(1, len(s)):
        if r[i-1] > 0:
            w[-1] += s[i]
        else:
            w.append(s[i])
    return w

words = defaultdict(int)
for t in texts():
    for i in cut(t):
        words[i] += 1

words = {i:j for i,j in words.items() if j >= min_count}


def is_real(s):
    if len(s) >= 3:
        for i in range(3, n+1):
            for j in range(len(s)-i+1):
                if s[j:j+i] not in ngrams_:
                    return False
        return True
    else:
        return True

w = {i:j for i,j in words.items() if is_real(i)}


# %load discover.py
#================================================================
#   Copyright (C) 2019 UltraPower Ltd. All rights reserved.
#   file: discover.py
#   mail: qinhaining@ultrapower.com.cn
#   date: 2019-05-13
#   describe:
#================================================================

from collections import defaultdict
import numpy as np


def gen():
    lines = open('/home/siy/data/广电全量地址_weak.csv','r').readlines()
    for line in lines:
        yield line
texts = gen

n = 4
min_count = 128
ngrams = defaultdict(int)

for t in texts():
    for i in range(len(t)):
        for j in range(1, n+1):
            if i+j <= len(t):
                ngrams[t[i:i+j]] += 1

ngrams = {i:j for i,j in ngrams.iteritems() if j >= min_count}
total = 1.*sum([j for i,j in ngrams.items() if len(i) == 1])

n0 = 5
min_proba = {2:n0, 3:n0**2, 4:n0**3}

def is_keep(s, min_proba):
    if len(s) >= 2:
        score = min([total*ngrams[s]/(ngrams[s[:i+1]]*ngrams[s[i+1:]]) for i in range(len(s)-1)])
        if score > min_proba[len(s)]:
            return True
    else:
        return False

ngrams_ = set(i for i,j in ngrams.items() if is_keep(i, min_proba))


def cut(s):
    r = np.array([0]*(len(s)-1))
    for i in range(len(s)-1):
        for j in range(2, n+1):
            if s[i:i+j] in ngrams_:
                r[i:i+j-1] += 1
    w = [s[0]]
    for i in range(1, len(s)):
        if r[i-1] > 0:
            w[-1] += s[i]
        else:
            w.append(s[i])
    return w

words = defaultdict(int)
for t in texts():
    for i in cut(t):
        words[i] += 1

words = {i:j for i,j in words.items() if j >= min_count}


def is_real(s):
    if len(s) >= 3:
        for i in range(3, n+1):
            for j in range(len(s)-i+1):
                if s[j:j+i] not in ngrams_:
                    return False
        return True
    else:
        return True

w = {i:j for i,j in words.items() if is_real(i)}


# %load discover.py
#================================================================
#   Copyright (C) 2019 UltraPower Ltd. All rights reserved.
#   file: discover.py
#   mail: qinhaining@ultrapower.com.cn
#   date: 2019-05-13
#   describe:
#================================================================

from collections import defaultdict
import numpy as np


def gen():
    lines = open('/home/siy/data/广电全量地址_weak.csv','r').readlines()
    for line in lines:
        yield line
texts = gen

n = 4
min_count = 128
ngrams = defaultdict(int)

for t in texts():
    for i in range(len(t)):
        for j in range(1, n+1):
            if i+j <= len(t):
                ngrams[t[i:i+j]] += 1

ngrams = {i:j for i,j in ngrams.items() if j >= min_count}
total = 1.*sum([j for i,j in ngrams.items() if len(i) == 1])

n0 = 5
min_proba = {2:n0, 3:n0**2, 4:n0**3}

def is_keep(s, min_proba):
    if len(s) >= 2:
        score = min([total*ngrams[s]/(ngrams[s[:i+1]]*ngrams[s[i+1:]]) for i in range(len(s)-1)])
        if score > min_proba[len(s)]:
            return True
    else:
        return False

ngrams_ = set(i for i,j in ngrams.items() if is_keep(i, min_proba))


def cut(s):
    r = np.array([0]*(len(s)-1))
    for i in range(len(s)-1):
        for j in range(2, n+1):
            if s[i:i+j] in ngrams_:
                r[i:i+j-1] += 1
    w = [s[0]]
    for i in range(1, len(s)):
        if r[i-1] > 0:
            w[-1] += s[i]
        else:
            w.append(s[i])
    return w

words = defaultdict(int)
for t in texts():
    for i in cut(t):
        words[i] += 1

words = {i:j for i,j in words.items() if j >= min_count}


def is_real(s):
    if len(s) >= 3:
        for i in range(3, n+1):
            for j in range(len(s)-i+1):
                if s[j:j+i] not in ngrams_:
                    return False
        return True
    else:
        return True

w = {i:j for i,j in words.items() if is_real(i)}


# %load discover.py
#================================================================
#   Copyright (C) 2019 UltraPower Ltd. All rights reserved.
#   file: discover.py
#   mail: qinhaining@ultrapower.com.cn
#   date: 2019-05-13
#   describe:
#================================================================

from collections import defaultdict
import numpy as np


def gen():
    lines = open('/home/siy/data/广电全量地址_weak.csv','r').readlines()
    for line in lines:
        yield line
texts = gen

n = 4
min_count = 128
ngrams = defaultdict(int)

for t in texts():
    for i in range(len(t)):
        for j in range(1, n+1):
            if i+j <= len(t):
                ngrams[t[i:i+j]] += 1

ngrams = {i:j for i,j in ngrams.items() if j >= min_count}
total = 1.*sum([j for i,j in ngrams.items() if len(i) == 1])

n0 = 5
min_proba = {2:n0, 3:n0**2, 4:n0**3}

def is_keep(s, min_proba):
    if len(s) >= 2:
        score = min([total*ngrams[s]/(ngrams[s[:i+1]]*ngrams[s[i+1:]]) for i in range(len(s)-1)])
        if score > min_proba[len(s)]:
            return True
    else:
        return False

ngrams_ = set(i for i,j in ngrams.items() if is_keep(i, min_proba))


def cut(s):
    r = np.array([0]*(len(s)-1))
    for i in range(len(s)-1):
        for j in range(2, n+1):
            if s[i:i+j] in ngrams_:
                r[i:i+j-1] += 1
    w = [s[0]]
    for i in range(1, len(s)):
        if r[i-1] > 0:
            w[-1] += s[i]
        else:
            w.append(s[i])
    return w


words = defaultdict(int)
for t in texts():
    for i in cut(t):
        words[i] += 1

        
words = {i:j for i,j in words.items() if j >= min_count}


def is_real(s):
    if len(s) >= 3:
        for i in range(3, n+1):
            for j in range(len(s)-i+1):
                if s[j:j+i] not in ngrams_:
                    return False
        return True
    else:
        return True

w = {i:j for i,j in words.items() if is_real(i)}


w
# %load discover.py
#================================================================
#   Copyright (C) 2019 UltraPower Ltd. All rights reserved.
#   file: discover.py
#   mail: qinhaining@ultrapower.com.cn
#   date: 2019-05-13
#   describe:
#================================================================

from collections import defaultdict
import numpy as np


def gen():
    lines = open('/home/siy/data/广电全量地址_weak.csv','r').readlines()
    for line in lines:
        yield line
texts = gen

n = 5
min_count = 128
ngrams = defaultdict(int)

for t in texts():
    for i in range(len(t)):
        for j in range(1, n+1):
            if i+j <= len(t):
                ngrams[t[i:i+j]] += 1

ngrams = {i:j for i,j in ngrams.items() if j >= min_count}
total = 1.*sum([j for i,j in ngrams.items() if len(i) == 1])

n0 = 6
min_proba = {2:n0, 3:n0**2, 4:n0**3}

def is_keep(s, min_proba):
    if len(s) >= 2:
        score = min([total*ngrams[s]/(ngrams[s[:i+1]]*ngrams[s[i+1:]]) for i in range(len(s)-1)])
        if score > min_proba[len(s)]:
            return True
    else:
        return False

ngrams_ = set(i for i,j in ngrams.items() if is_keep(i, min_proba))


def cut(s):
    r = np.array([0]*(len(s)-1))
    for i in range(len(s)-1):
        for j in range(2, n+1):
            if s[i:i+j] in ngrams_:
                r[i:i+j-1] += 1
    w = [s[0]]
    for i in range(1, len(s)):
        if r[i-1] > 0:
            w[-1] += s[i]
        else:
            w.append(s[i])
    return w


words = defaultdict(int)
for t in texts():
    for i in cut(t):
        words[i] += 1

        
words = {i:j for i,j in words.items() if j >= min_count}


def is_real(s):
    if len(s) >= 3:
        for i in range(3, n+1):
            for j in range(len(s)-i+1):
                if s[j:j+i] not in ngrams_:
                    return False
        return True
    else:
        return True

w = {i:j for i,j in words.items() if is_real(i)}


# %load discover.py
#================================================================
#   Copyright (C) 2019 UltraPower Ltd. All rights reserved.
#   file: discover.py
#   mail: qinhaining@ultrapower.com.cn
#   date: 2019-05-13
#   describe:
#================================================================

from collections import defaultdict
import numpy as np


def gen():
    lines = open('/home/siy/data/广电全量地址_weak.csv','r').readlines()
    np.random.shuffle(lines)
    for line in lines[:100]:
        yield line
texts = gen

n = 5
min_count = 128
ngrams = defaultdict(int)

for t in texts():
    for i in range(len(t)):
        for j in range(1, n+1):
            if i+j <= len(t):
                ngrams[t[i:i+j]] += 1

ngrams = {i:j for i,j in ngrams.items() if j >= min_count}
total = 1.*sum([j for i,j in ngrams.items() if len(i) == 1])

n0 = 6
min_proba = {2:n0, 3:n0**2, 4:n0**3}

def is_keep(s, min_proba):
    if len(s) >= 2:
        score = min([total*ngrams[s]/(ngrams[s[:i+1]]*ngrams[s[i+1:]]) for i in range(len(s)-1)])
        if score > min_proba[len(s)]:
            return True
    else:
        return False

ngrams_ = set(i for i,j in ngrams.items() if is_keep(i, min_proba))


def cut(s):
    r = np.array([0]*(len(s)-1))
    for i in range(len(s)-1):
        for j in range(2, n+1):
            if s[i:i+j] in ngrams_:
                r[i:i+j-1] += 1
    w = [s[0]]
    for i in range(1, len(s)):
        if r[i-1] > 0:
            w[-1] += s[i]
        else:
            w.append(s[i])
    return w


words = defaultdict(int)
for t in texts():
    for i in cut(t):
        words[i] += 1

        
words = {i:j for i,j in words.items() if j >= min_count}


def is_real(s):
    if len(s) >= 3:
        for i in range(3, n+1):
            for j in range(len(s)-i+1):
                if s[j:j+i] not in ngrams_:
                    return False
        return True
    else:
        return True

w = {i:j for i,j in words.items() if is_real(i)}


w
# %load discover.py
#================================================================
#   Copyright (C) 2019 UltraPower Ltd. All rights reserved.
#   file: discover.py
#   mail: qinhaining@ultrapower.com.cn
#   date: 2019-05-13
#   describe:
#================================================================

from collections import defaultdict
import numpy as np


def gen():
    lines = open('/home/siy/data/广电全量地址_weak.csv','r').readlines()
    np.random.shuffle(lines)
    for line in lines[:100]:
        yield line
texts = gen

n = 5
min_count = 10
ngrams = defaultdict(int)

for t in texts():
    for i in range(len(t)):
        for j in range(1, n+1):
            if i+j <= len(t):
                ngrams[t[i:i+j]] += 1

ngrams = {i:j for i,j in ngrams.items() if j >= min_count}
total = 1.*sum([j for i,j in ngrams.items() if len(i) == 1])

n0 = 6
min_proba = {2:n0, 3:n0**2, 4:n0**3}

def is_keep(s, min_proba):
    if len(s) >= 2:
        score = min([total*ngrams[s]/(ngrams[s[:i+1]]*ngrams[s[i+1:]]) for i in range(len(s)-1)])
        if score > min_proba[len(s)]:
            return True
    else:
        return False

ngrams_ = set(i for i,j in ngrams.items() if is_keep(i, min_proba))


def cut(s):
    r = np.array([0]*(len(s)-1))
    for i in range(len(s)-1):
        for j in range(2, n+1):
            if s[i:i+j] in ngrams_:
                r[i:i+j-1] += 1
    w = [s[0]]
    for i in range(1, len(s)):
        if r[i-1] > 0:
            w[-1] += s[i]
        else:
            w.append(s[i])
    return w


words = defaultdict(int)
for t in texts():
    for i in cut(t):
        words[i] += 1

        
words = {i:j for i,j in words.items() if j >= min_count}


def is_real(s):
    if len(s) >= 3:
        for i in range(3, n+1):
            for j in range(len(s)-i+1):
                if s[j:j+i] not in ngrams_:
                    return False
        return True
    else:
        return True

w = {i:j for i,j in words.items() if is_real(i)}


w
# %load discover.py
#================================================================
#   Copyright (C) 2019 UltraPower Ltd. All rights reserved.
#   file: discover.py
#   mail: qinhaining@ultrapower.com.cn
#   date: 2019-05-13
#   describe:
#================================================================

from collections import defaultdict
import numpy as np


def gen():
    lines = open('/home/siy/data/广电全量地址_weak.csv','r').readlines()
    np.random.shuffle(lines)
    for line in lines[:100]:
        yield line
texts = gen

n = 4
min_count = 10
ngrams = defaultdict(int)

for t in texts():
    for i in range(len(t)):
        for j in range(1, n+1):
            if i+j <= len(t):
                ngrams[t[i:i+j]] += 1

ngrams = {i:j for i,j in ngrams.items() if j >= min_count}
total = 1.*sum([j for i,j in ngrams.items() if len(i) == 1])

n0 = 6
min_proba = {2:n0, 3:n0**2, 4:n0**3}

def is_keep(s, min_proba):
    if len(s) >= 2:
        score = min([total*ngrams[s]/(ngrams[s[:i+1]]*ngrams[s[i+1:]]) for i in range(len(s)-1)])
        if score > min_proba[len(s)]:
            return True
    else:
        return False

ngrams_ = set(i for i,j in ngrams.items() if is_keep(i, min_proba))


def cut(s):
    r = np.array([0]*(len(s)-1))
    for i in range(len(s)-1):
        for j in range(2, n+1):
            if s[i:i+j] in ngrams_:
                r[i:i+j-1] += 1
    w = [s[0]]
    for i in range(1, len(s)):
        if r[i-1] > 0:
            w[-1] += s[i]
        else:
            w.append(s[i])
    return w


words = defaultdict(int)
for t in texts():
    for i in cut(t):
        words[i] += 1

        
words = {i:j for i,j in words.items() if j >= min_count}


def is_real(s):
    if len(s) >= 3:
        for i in range(3, n+1):
            for j in range(len(s)-i+1):
                if s[j:j+i] not in ngrams_:
                    return False
        return True
    else:
        return True

w = {i:j for i,j in words.items() if is_real(i)}


w
is_real('毕节地区')
is_real('毕节地区人民法院')
words.item
words.items()
# %load discover.py
#================================================================
#   Copyright (C) 2019 UltraPower Ltd. All rights reserved.
#   file: discover.py
#   mail: qinhaining@ultrapower.com.cn
#   date: 2019-05-13
#   describe:
#================================================================

from collections import defaultdict
import numpy as np


def gen():
    lines = open('/home/siy/data/广电全量地址_weak.csv','r').readlines()
    np.random.shuffle(lines)
    for line in lines[:100]:
        yield line
texts = gen

n = 4
min_count = 10
ngrams = defaultdict(int)

for t in texts():
    for i in range(len(t)):
        for j in range(1, n+1):
            if i+j <= len(t):
                ngrams[t[i:i+j]] += 1

ngrams = {i:j for i,j in ngrams.items() if j >= min_count}
total = 1.*sum([j for i,j in ngrams.items() if len(i) == 1])

n0 = 6
min_proba = {2:n0, 3:n0**2, 4:n0**3}

def is_keep(s, min_proba):
    if len(s) >= 2:
        score = min([total*ngrams[s]/(ngrams[s[:i+1]]*ngrams[s[i+1:]]) for i in range(len(s)-1)])
        if score > min_proba[len(s)]:
            return True
    else:
        return False

ngrams_ = set(i for i,j in ngrams.items() if is_keep(i, min_proba))


def cut(s):
    r = np.array([0]*(len(s)-1))
    for i in range(len(s)-1):
        for j in range(2, n+1):
            if s[i:i+j] in ngrams_:
                r[i:i+j-1] += 1
    w = [s[0]]
    for i in range(1, len(s)):
        if r[i-1] > 0:
            w[-1] += s[i]
        else:
            w.append(s[i])
    return w


words = defaultdict(int)
for t in texts():
    for i in cut(t):
        words[i] += 1

        
words = {i:j for i,j in words.items() if j >= min_count}


def is_real(s):
    if len(s) >= 4:
        for i in range(4, n+1):
            for j in range(len(s)-i+1):
                if s[j:j+i] not in ngrams_:
                    return False
        return True
    else:
        return True

w = {i:j for i,j in words.items() if is_real(i)}


w
# %load discover.py
#================================================================
#   Copyright (C) 2019 UltraPower Ltd. All rights reserved.
#   file: discover.py
#   mail: qinhaining@ultrapower.com.cn
#   date: 2019-05-13
#   describe:
#================================================================

from collections import defaultdict
import numpy as np


def gen():
    lines = open('/home/siy/data/广电全量地址_weak.csv','r').readlines()
    np.random.shuffle(lines)
    for line in lines[:100]:
        yield line
texts = gen

n = 4
min_count = 10
ngrams = defaultdict(int)

for t in texts():
    for i in range(len(t)):
        for j in range(1, n+1):
            if i+j <= len(t):
                ngrams[t[i:i+j]] += 1

ngrams = {i:j for i,j in ngrams.items() if j >= min_count}
total = 1.*sum([j for i,j in ngrams.items() if len(i) == 1])

n0 = 6
min_proba = {2:n0, 3:n0**2, 4:n0**3}

def is_keep(s, min_proba):
    if len(s) >= 2:
        score = min([total*ngrams[s]/(ngrams[s[:i+1]]*ngrams[s[i+1:]]) for i in range(len(s)-1)])
        if score > min_proba[len(s)]:
            return True
    else:
        return False

ngrams_ = set(i for i,j in ngrams.items() if is_keep(i, min_proba))


def cut(s):
    r = np.array([0]*(len(s)-1))
    for i in range(len(s)-1):
        for j in range(2, n+1):
            if s[i:i+j] in ngrams_:
                r[i:i+j-1] += 1
    w = [s[0]]
    for i in range(1, len(s)):
        if r[i-1] > 0:
            w[-1] += s[i]
        else:
            w.append(s[i])
    return w


words = defaultdict(int)
for t in texts():
    for i in cut(t):
        words[i] += 1

        
words = {i:j for i,j in words.items() if j >= min_count}


def is_real(s):
    if len(s) >= 5:
        for i in range(5, n+1):
            for j in range(len(s)-i+1):
                if s[j:j+i] not in ngrams_:
                    return False
        return True
    else:
        return True

w = {i:j for i,j in words.items() if is_real(i)}


w
# %load discover.py
#================================================================
#   Copyright (C) 2019 UltraPower Ltd. All rights reserved.
#   file: discover.py
#   mail: qinhaining@ultrapower.com.cn
#   date: 2019-05-13
#   describe:
#================================================================

from collections import defaultdict
import numpy as np


def gen():
    lines = open('/home/siy/data/广电全量地址_weak.csv','r').readlines()
    np.random.shuffle(lines)
    for line in lines[:100]:
        yield line[::-1]
texts = gen

n = 4
min_count = 10
ngrams = defaultdict(int)

for t in texts():
    for i in range(len(t)):
        for j in range(1, n+1):
            if i+j <= len(t):
                ngrams[t[i:i+j]] += 1

ngrams = {i:j for i,j in ngrams.items() if j >= min_count}
total = 1.*sum([j for i,j in ngrams.items() if len(i) == 1])

n0 = 6
min_proba = {2:n0, 3:n0**2, 4:n0**3}

def is_keep(s, min_proba):
    if len(s) >= 2:
        score = min([total*ngrams[s]/(ngrams[s[:i+1]]*ngrams[s[i+1:]]) for i in range(len(s)-1)])
        if score > min_proba[len(s)]:
            return True
    else:
        return False

ngrams_ = set(i for i,j in ngrams.items() if is_keep(i, min_proba))


def cut(s):
    r = np.array([0]*(len(s)-1))
    for i in range(len(s)-1):
        for j in range(2, n+1):
            if s[i:i+j] in ngrams_:
                r[i:i+j-1] += 1
    w = [s[0]]
    for i in range(1, len(s)):
        if r[i-1] > 0:
            w[-1] += s[i]
        else:
            w.append(s[i])
    return w


words = defaultdict(int)
for t in texts():
    for i in cut(t):
        words[i] += 1

        
words = {i:j for i,j in words.items() if j >= min_count}


def is_real(s):
    if len(s) >= 5:
        for i in range(5, n+1):
            for j in range(len(s)-i+1):
                if s[j:j+i] not in ngrams_:
                    return False
        return True
    else:
        return True

w = {i:j for i,j in words.items() if is_real(i)}


w
get_ipython().run_line_magic('ed', 'discover.py')
get_ipython().run_line_magic('ed', 'discover.py')
