# -*- coding: utf-8 -*-

import filecmp
import os
import shutil
import threading
import time
import unittest

import stromx.cvsupport
import stromx.runtime
import stromx.test

import model

_packages = [
    'libstromx_runtime.so.0.8.0',
    'libstromx_cvsupport.so.0.8.0',
    'libstromx_test.so.0.8.0'
]

_content = (
"""
data:;base64,UEsDBBQAAAAIAIya1EgdpDSCGQIAAKUIAAAKAAAAc3RyZWFtLnhtbL1WTW/bMAy951d
w2mU7pP7qoQcnRZegQIZtLbAU61Wx1VSoLBmyPMT79aMtx0kM28maYD4Yoii+Jz5alMPbTSLgN9MZV3J
CvCuXAJORirlcT8jT8n58QyAzVMZUKMkmRCoCt9NR+NNolWx2ke6Vj7HT0Qig9DGagKQJBuAc4BM+pEx
TozTwGFcT4NlCcsOp4H8YzhidM1KHzPMkJZDS6I2u0dS5NDxBrynSxrtHXG16U4EW5dsSIuVCprnZ8qm
aH5NEIzfosvPVcMmNQOyHykAma1YAxKkzcLYpdGXkDWb0VXHZn5H1npLRI9WIZ1jDWW/0R56scFK9AC+
3nDURGDOnhvZSPy2kCfwD8puyjn7olHENsdMwd6jr76vr79T1O9UF91BftJ0O0KAHNOgG9Vqg3mll8wf
Ldq/0W3/ZrPcyZbMp/ee6HZyK653E3sVORTAo70xhUkz3K9wsGBDZ6eK9HuR9ZJpjh4vmTNCin721rCX
1CYX2G8ksFHxKuBA8Y5GScfb57GJ7ruu+u97Bhbrg8hWbfQyREiXqR7d6tkrXzrtWT54pKVlUFUtud1C
NlvuMBx+ncyaCfzbC7lNzbFr/IMCXYwL4HeTQurXeTz87Rh900XtH6UPHXvV47VdD/CPAX4MP4/Hz92+
wZrIMZjHQ3KiEGh5RIQpYFfCciF+aG9v6zCsreSRkKtcRA8FXmuoCLN54PB39BVBLAQIAABQAAAAIAIy
a1EgdpDSCGQIAAKUIAAAKAAAAAAAAAAAAAAAAAAAAAABzdHJlYW0ueG1sUEsFBgAAAAABAAEAOAAAAEE
CAAAAAA==
""")

_colorImage = (
"""
data:image/jpg;base64,/9j/4AAQSkZJRgABAQAAAQABAAD/2wBDAAIBAQEBAQIBAQECAgICAgQDAg
ICAgUEBAMEBgUGBgYFBgYGBwkIBgcJBwYGCAsICQoKCgoKBggLDAsKDAkKCgr/2wBDAQICAgICAgUDAw
UKBwYHCgoKCgoKCgoKCgoKCgoKCgoKCgoKCgoKCgoKCgoKCgoKCgoKCgoKCgoKCgoKCgoKCgr/wAARCA
ANAAwDASIAAhEBAxEB/8QAHwAAAQUBAQEBAQEAAAAAAAAAAAECAwQFBgcICQoL/8QAtRAAAgEDAwIEAw
UFBAQAAAF9AQIDAAQRBRIhMUEGE1FhByJxFDKBkaEII0KxwRVS0fAkM2JyggkKFhcYGRolJicoKSo0NT
Y3ODk6Q0RFRkdISUpTVFVWV1hZWmNkZWZnaGlqc3R1dnd4eXqDhIWGh4iJipKTlJWWl5iZmqKjpKWmp6
ipqrKztLW2t7i5usLDxMXGx8jJytLT1NXW19jZ2uHi4+Tl5ufo6erx8vP09fb3+Pn6/8QAHwEAAwEBAQ
EBAQEBAQAAAAAAAAECAwQFBgcICQoL/8QAtREAAgECBAQDBAcFBAQAAQJ3AAECAxEEBSExBhJBUQdhcR
MiMoEIFEKRobHBCSMzUvAVYnLRChYkNOEl8RcYGRomJygpKjU2Nzg5OkNERUZHSElKU1RVVldYWVpjZG
VmZ2hpanN0dXZ3eHl6goOEhYaHiImKkpOUlZaXmJmaoqOkpaanqKmqsrO0tba3uLm6wsPExcbHyMnK0t
PU1dbX2Nna4uPk5ebn6Onq8vP09fb3+Pn6/9oADAMBAAIRAxEAPwCz8GfHXgq8+LB8D+L9Kk119cs2n1
BvO8pdOjfb/pZdfm3Nldir/ErbtqbmqK1/Z00H9qeSf4wa34g8aQ2N3N9m8PQQX8kMi2EKiNHm+zoEZ5
XWWcf3Y5o0HCCvNfgvp51T9rq88O6jcyNY6RHNH5MEjRm4hNtZR+W7Kc8clW6rnjFd/wCLP20fjT+zBq
rfBv4Mapb2GjaRJNbql5ZQ3LyNFPJAr7nTK/uoolxzypP8VfL1cLVw1WNHApOpyxd3ppKPM/0+4/prF1
8TiYrERfxOSSbsrRdul9T/2Q==
""")

_parallelFile = {
    'id': '0',
    'name': '0_parallel.stromx',
    'content': '',
    'opened': False,
    'saved' : False,
    'stream': None
}

_renamedFile = {
    'id': '0',
    'name': 'renamed.stromx',
    'content': '',
    'opened': False,
    'saved' : False,
    'stream': None
}

_openedFile = {'id': '0', 
    'name': '0_parallel.stromx', 
    'content': '',
    'opened': True, 
    'saved' : False,
    'stream': '0'
}

_testFile = {'id': '1', 
    'name': 'test.stromx', 
    'content': '', 
    'opened': False,
    'saved' : False,
    'stream': None
}

_noFile = {'id': '1', 
    'name': 'nothing.stromx', 
    'content': '', 
    'opened': False,
    'saved' : False,
    'stream': None
}

_stream = {
    'id': '0',
    'name': '',
    'active': False,
    'paused': False,
    'file': '0',
    'connections': ['0', '1', '2', '3', '4'],
    'operators': ['0', '1', '2', '3', '4'],
    'views': []
}

_fork = {
    'status': 'initialized',
    'name': 'Fork',
    'parameters': ['1'],
    'package': 'runtime',
    'outputs': ['1', '2'],
    'inputs': ['3'],
    'version': '0.8.0',
    'position': {'y': 0.0, 'x': 0.0},
    'type': 'Fork', 'id': '2',
    'stream': '0'
}

class ErrorSink(object):
    def __init__(self):
        self.__lock = threading.Lock()
        self.errors = []
        
    def handleError(self, error):
        with self.__lock:
            self.errors.append(error)

class DummyItems(model.Items):
    pass

class DummyItem(model.Item):
    _properties = ['read', 'write']
    
    def __init__(self):
        super(DummyItem, self).__init__()
        self.__write = 0
    
    @property
    def read(self):
        return 0
    
    @property
    def write(self):
        return self.__write
    
    @write.setter
    def write(self, value):
        self.__write = value
    
class ItemTest(unittest.TestCase):
    def setUp(self):
        self.items = DummyItems()
        self.item = DummyItem()
        self.items.addItem(self.item)
        
    def testData(self):
        self.assertEqual({'dummyItem': {'read': 0, 'write': 0, 'id': '0'}},
                         self.item.data)
        
    def testSet(self):
        self.item.set({'dummyItem': {'read': 0, 'write': 0}})
    
    
class ItemsTest(unittest.TestCase):
    def setUp(self):
        self.items = DummyItems()
        
    def testDelete(self):
        item = DummyItem()
        self.items.addItem(item)
        self.items.delete(item.index)
        self.assertFalse(item.index in self.items.keys())
        
class OperatorTemplatesTest(unittest.TestCase):
    def setUp(self):
        shutil.rmtree('temp', True)
        shutil.copytree('data/stream', 'temp')
        self.model = model.Model('temp', _packages)
        self.templates = self.model.operatorTemplates
        
    def testData(self):
        refData = {'operatorTemplate': {'id': '0',
                                        'package': 'runtime',
                                        'type': 'Block',
                                        'version': '0.8.0'}}
                                         
        self.assertEqual(31, len(self.templates)) 
        self.assertEqual(refData, self.templates['0'].data)

class FilesTest(unittest.TestCase):
    def setUp(self):
        shutil.rmtree('temp', True)
        shutil.copytree('data/stream', 'temp')
        
        self.model = model.Model('temp', _packages)
        self.files = self.model.files
        self.streams = self.model.streams
        self.errorSink = ErrorSink()

    def testData(self):
        self.assertEqual({'files': [_parallelFile]}, self.files.data)

    def testDelete(self):
        self.files.delete('0')
        self.assertEqual({'files': []}, self.files.data)
        self.assertFalse(os.path.exists('temp/parallel.stromx'))
    
    def testDeleteEmptyFile(self):
        self.files.addData({'file': {'name': 'test.stromx'}})
        self.files.delete('1')
        self.assertEqual(1, len(self.files))
    
    def testDeleteOpenedFile(self):
        self.files.set('0', {'file': {'opened': True}})
        self.files.delete('0')
        self.assertEqual({'streams': []}, self.streams.data)
            
    def testGetItem(self):
        self.assertEqual({'file': _parallelFile}, 
                         self.files['0'].data)
        
    def testSetOpenTrue(self):
        f = self.files.set('0', {'file': {'opened': True}})
        self.assertEqual({'file': _openedFile}, f)
        self.assertEqual({'stream': _stream}, self.streams['0'].data)
        
    def testSetOpenFalse(self):
        self.files.set('0', {'file': {'opened': True}})
        f = self.files.set('0', {'file': {'opened': False}})
        self.assertEqual(False, f['file']['opened'])
        self.assertEqual({'streams': []}, self.streams.data)
        
    def testSetOpenFalseWhileActive(self):
        self.files.set('0', {'file': {'opened': True}})
        self.streams.set('0', {'stream': {'active': True}})
        
        f = self.files.set('0', {'file': {'opened': False}})
                          
        self.assertEqual(False, f['file']['opened'])
        self.assertEqual({'streams': []}, self.streams.data)
        
    def testStopStreamAndSetOpenFalse(self):
        self.files.set('0', {'file': {'opened': True}})
        self.streams.set('0', {'stream': {'active': True}})
        self.streams.set('0', {'stream': {'active': False}})
        
        f = self.files.set('0', {'file': {'opened': False}})
        
        self.assertEqual(False, f['file']['opened'])
        self.assertEqual({'streams': []}, self.streams.data)
        
    def testSetOpenFails(self):
        shutil.rmtree('temp', True)
        os.mkdir('temp')
        with open('temp/invalid.stromx', 'w') as f:
            f.write("nonsense")
        self.model = model.Model('temp', _packages)
        self.files = self.model.files
        self.model.errors.addHandler(self.errorSink.handleError)
                 
        self.assertRaises(model.Failed, self.files.set, 
                          '0', {'file': {'opened': True}})
           
        f = self.files['0'].data
        self.assertEqual(False, f['file']['opened'])
        self.assertEqual(1, len(self.errorSink.errors))
        
    def testSetName(self):
        f = self.files.set('0', {'file': {'name': 'renamed.stromx'}})
        self.assertEqual({'file': _renamedFile}, f)
        self.assertTrue(os.path.exists('temp/renamed.stromx'))
        self.assertFalse(os.path.exists('temp/parallel.stromx'))
        
    def testSetNameWithInsecurePath(self):
        f = self.files.set('0', {'file': {'name': '../renamed.stromx'}})
        self.assertEqual({'file': _renamedFile}, f)
        self.assertTrue(os.path.exists('temp/renamed.stromx'))
        self.assertFalse(os.path.exists('temp/parallel.stromx'))
        
    def testSetNameEmpty(self):
        f = self.files.set('0', {'file': {'name': ''}})
        self.assertEqual({'file': _parallelFile}, f)
        
    def testAddNoContent(self):
        self.files.addData({'file': {'name': 'test.stromx'}})
        self.assertEqual({'files': [_testFile, _parallelFile]},
                         self.files.data)
        self.assertFalse(os.path.exists('temp/test.stromx'))
        
    def testAddNoneContent(self):
        self.files.addData({'file': {'name': 'test.stromx', 'content': None}})
        self.assertEqual({'files': [_testFile, _parallelFile]},
                         self.files.data)
        self.assertFalse(os.path.exists('temp/test.stromx'))
        
    def testAddOpenedNoneContent(self):
        fileData = self.files.addData({'file': {
            'name': 'test.stromx',
            'content': None, 
            'opened': True
        }})
        self.assertEqual(True, fileData['file']['opened'])
        self.assertEqual('0', fileData['file']['stream'])
        
    def testSetSavedStreamName(self):
        self.files['0'].opened = True
        self.streams.set('0', {'stream': {'name': 'New name'}})
        
        self.files.set('0', {'file': {'saved': True}})
        
        self.files['0'].opened = False
        self.files['0'].opened = True
        self.assertEqual('New name', self.streams.data['streams'][0]['name'])    
    
    def testSetSaved(self):
        self.files['0'].opened = True
        
        self.files.set('0', {'file': {'saved': True}})
        
        self.assertFalse(self.files.data['files'][0]['saved'])   
    
    def testSetSavedAndOpened(self):
        self.files['0'].opened = True
        
        self.files.set('0', {'file': {'opened': False, 'saved': True}})
        
        self.assertFalse(self.files.data['files'][0]['saved'])
        self.assertFalse(self.files.data['files'][0]['opened'])
        
    def testSetSavedNewFile(self):
        data = self.model.files.addData({'file': {'name': u'new.stromx'}})
        newFile = self.model.files[data['file']['id']]
        newFile.opened = True 
        fileIndex = newFile.index
        
        self.files.set(fileIndex, {'file': {'saved': True}})
        
        self.assertTrue(os.path.exists('temp/new.stromx'))
        
    def testAddContent(self):
        self.files.addData({'file': {'name': 'test.stromx',
                                     'content': _content}})
        self.assertEqual({'files': [_testFile, _parallelFile]}, self.files.data)
        self.assertTrue(os.path.exists('temp/test.stromx'))
        self.assertTrue(filecmp.cmp('data/stream/0_parallel.stromx',
                                    'temp/test.stromx'))
        
    def testAddContentOpened(self):
        fileData = self.files.addData({'file': {'name': 'test.stromx',
                                                'opened': True,
                                                'content': _content}})
        self.assertEqual(True, fileData['file']['opened'])
        self.assertEqual('0', fileData['file']['stream'])
        
    def testAddDuplicate(self):
        self.files.addData({'file': {'name': '0_parallel.stromx'}})
        self.assertEqual({'files': [_parallelFile]}, self.files.data)
        self.assertFalse(os.path.exists('temp/0_parallel.stromx'))
        
    def testAddWithInsecurePath(self):
        self.files.addData({'file': {'name': '../test.stromx',
                                     'content': _content}})
        self.assertEqual({'files': [_testFile, _parallelFile]}, self.files.data)
        self.assertTrue(os.path.exists('temp/test.stromx'))
        self.assertTrue(filecmp.cmp('data/stream/0_parallel.stromx',
                                    'temp/test.stromx'))
        
    def testSecureName(self):
        self.assertEqual('test.stromx',
                         model.File.secureName('test.stromx'))
        
    def testSecureNameUnicode(self):
        self.assertEqual('test.stromx',
                         model.File.secureName(u'test.stromx'))
                                    
    def testSecureNameUpDirectory(self):
        self.assertEqual('test.stromx', model.File.secureName('../test.stromx'))
        
    def testSecureNameDownDirectory(self):
        self.assertEqual('test.stromx',
                         model.File.secureName('dir/test.stromx'))
        
    def testSecureNameNoStromxSuffix(self):
        self.assertEqual('test.stromx',
                         model.File.secureName('test'))
        
    def testSecureNameStartsWithDot(self):
        self.assertEqual('test.stromx',
                         model.File.secureName('..test.stromx'))
        
    def testSecureNameContainsBackslash(self):
        self.assertEqual('test.stromx',
                         model.File.secureName('\\test.stromx'))
        
    def testSecureNameEmpty(self):
        self.assertEqual('', model.File.secureName(''))
        
    def tearDown(self):
        shutil.rmtree('temp', True)
        
class StreamsTest(unittest.TestCase):
    def setUp(self):
        shutil.rmtree('temp', True)
        self.errorSink = ErrorSink()
        
    def setUpStream(self):
        shutil.copytree('data/stream', 'temp')
        
        self.model = model.Model('temp', _packages)
        self.streams = self.model.streams
        self.streamFile = self.model.files['0']
        
    def setUpDeinitialized(self):
        shutil.copytree('data/deinitialized', 'temp')
        
        self.model = model.Model('temp', _packages)
        self.streams = self.model.streams
        self.streamFile = self.model.files['0']
        
    def setUpException(self):
        shutil.copytree('data/exception', 'temp')
        
        self.model = model.Model('temp', _packages)
        self.model.errors.addHandler(self.errorSink.handleError)
        self.streams = self.model.streams
        self.activateFile = self.model.files['0']
        self.deactivateFile = self.model.files['1']
        self.deinitializeFile = self.model.files['2']
        self.executeFile = self.model.files['3']
        
    def setUpViews(self):
        shutil.copytree('data/views', 'temp')
        
        self.model = model.Model('temp', _packages)
        self.streams = self.model.streams
        self.streamFile = self.model.files['0']
        
    def testAddData(self):
        self.setUpStream()
        self.streamFile.opened = True
        self.assertEqual({'streams': [_stream]}, self.streams.data)
        
        self.assertEqual(5, len(self.model.operators))
        for op in self.model.operators.values():
            self.assertEqual('0', op.stream)
            
        self.assertEqual(5, len(self.model.inputs))
        self.assertEqual(5, len(self.model.outputs))
        self.assertEqual(5, len(self.model.connections))
        self.assertEqual({'operator': _fork}, self.model.operators['2'].data)
        
    def testAddDataDeinitialized(self):
        self.setUpDeinitialized()
        self.streamFile.opened = True
        
        self.assertEqual(True, self.streamFile.data['file']['opened'])
        
    def testAddNoFile(self):
        self.setUpStream()
        files = self.model.files
        files.addData({'file': _noFile})
        self.streams.addFile(files['1'])
        
    def testSetActivate(self):
        self.setUpStream()
        self.streamFile.opened = True
        self.streams.set('0', {'stream': {'active': True}})
        
        self.assertTrue(self.streams.data['streams'][0]['active'])
        self.assertNotEqual(None, self.model.connections['0'].thread)
        self.assertNotEqual(None, self.model.connections['1'].thread)
        self.assertNotEqual(None, self.model.connections['2'].thread)
        self.assertNotEqual(None, self.model.connections['3'].thread)
        self.assertNotEqual(None, self.model.connections['4'].thread)
        
    def testSetActivateFails(self):
        self.setUpException()
        self.activateFile.opened = True
        
        self.assertRaises(model.Failed, self.streams.set, '0',
                          {'stream': {'active': True}})
        self.assertFalse(self.streams.data['streams'][0]['active'])
        self.assertEqual(1, len(self.errorSink.errors))
        
    def testExecuteFails(self):
        self.setUpException()
        self.executeFile.opened = True
        
        self.streams.set('0', {'stream': {'active': True}})
        time.sleep(1.3)
        
        self.assertEqual(1, len(self.errorSink.errors))
        self.assertEqual(
            'ExceptionOperator (test::ExceptionOperator) during EXECUTION: '
            'Failed to execute operator.',
            self.errorSink.errors[0].description
        )
        
    def testSetDeactivate(self):
        self.setUpStream()
        self.streamFile.opened = True
        self.streams.set('0', {'stream': {'active': True}})
        self.streams.set('0', {'stream': {'active': False}})
        self.assertFalse(self.streams.data['streams'][0]['active'])
        self.streams.set('0', {'stream': {'active': False}})
        
    def testSetDeactivateAfterFail(self):
        self.setUpException()
        self.activateFile.opened = True
        try:
            self.streams.set('0', {'stream': {'active': True}})
        except model.Failed:
            pass
            
        self.streams.set('0', {'stream': {'active': False}})
        
        self.assertFalse(self.streams.data['streams'][0]['active'])
        self.assertEqual(1, len(self.errorSink.errors))
        
    def testSetDeactivateTwice(self):
        self.setUpStream()
        self.streamFile.opened = True
        self.streams.set('0', {'stream': {'active': True}})
        self.streams.set('0', {'stream': {'active': False}})
        self.streams.set('0', {'stream': {'active': False}})
        
    def testSetDeactivateFails(self):
        self.setUpException()
        self.deactivateFile.opened = True
        self.streams.set('0', {'stream': {'active': True}})
        self.assertEqual(0, len(self.errorSink.errors))
        
        self.streams.set('0', {'stream': {'active': False}})
        
        self.assertEqual(1, len(self.errorSink.errors))
        self.assertEqual(
            'ExceptionOperator (test::ExceptionOperator) during DEACTIVATION: '
            'Failed to deactivate operator.',
            self.errorSink.errors[0].description
        )
        
    def testSetPause(self):
        self.setUpStream()
        self.streams.addFile(self.streamFile)
        self.streams.set('0', {'stream': {'active': True}})
        self.streams.set('0', {'stream': {'paused': True}})
        self.assertTrue(self.streams.data['streams'][0]['paused'])
        
    def testSetResume(self):
        self.setUpStream()
        self.streamFile.opened = True
        self.streams.set('0', {'stream': {'active': True}})
        self.streams.set('0', {'stream': {'paused': True}})
        self.streams.set('0', {'stream': {'paused': False}})
        self.assertFalse(self.streams.data['streams'][0]['paused'])
        
    def testSetName(self):
        self.setUpStream()
        self.streamFile.opened = True
        self.streams.set('0', {'stream': {'name': 'New name'}})
        self.assertEqual('New name', self.streams.data['streams'][0]['name'])
        
    def testDelete(self):
        self.setUpStream()
        self.streamFile.opened = True
        stream = self.streams['0']
        self.streams.delete(stream.index)
        self.assertEqual(dict(), self.model.operators)  
        self.assertEqual(dict(), self.model.connections) 
        
    def testReadViews(self):
        self.setUpViews()
        self.streamFile.opened = True
        stream = self.streams['0']
        self.assertEqual(['0'], stream.data['stream']['views'])
        
    def tearDown(self):
        shutil.rmtree('temp', True)
        
class OperatorsTest(unittest.TestCase):
    def setUp(self):
        self.model = model.Model(packages = _packages)
        self.errorSink = ErrorSink()
        self.model.errors.addHandler(self.errorSink.handleError)
        self.operators = self.model.operators
        
        fileModel = model.File("", self.model)
        self.stream = self.model.streams.addFile(fileModel)
        self.stromxStream = self.stream.stromxStream
        
        kernel = stromx.runtime.Block()
        self.stromxOp = self.stromxStream.addOperator(kernel)
        self.stromxStream.initializeOperator(self.stromxOp)
        self.stromxOp.setName('Name')
        self.operator = self.operators.addStromxOp(self.stromxOp, self.stream)
        self.stream.addOperator(self.operator)
        
    def testSetName(self):
        self.operators.set('0', {'operator': {'name': 'New name'}})
        self.assertEqual('New name',
                         self.operator.data['operator']['name'])
        
    def testSetNameUmlaut(self):
        self.operators.set('0', {'operator': {'name': u'\xe4'}})
        self.assertEqual('ä', self.operator.data['operator']['name'])
        
    def testSetPosition(self):
        self.operators.set('0', {'operator': 
                                 {'position': {'x': 20.5, 'y': 30.5}}
                                 })
        self.assertAlmostEqual(20.5,
                               self.operator.data['operator']['position']['x'])
        self.assertAlmostEqual(30.5,
                               self.operator.data['operator']['position']['y'])
        
    def testData(self):
        data = {'operator': {'id': '0', 
                             'name': 'Name',
                             'package': 'runtime',
                             'type': 'Block',
                             'status': 'initialized',
                             'version': '0.8.0',
                             'parameters': ['0', '1', '2'],
                             'outputs': ['0'],
                             'inputs': ['0'],
                             'position': {'x': 0.0, 'y': 0.0},
                             'stream': '0'}}
        self.assertEqual(data, self.operator.data)
        
    def testAddData(self):
        data = {'operator': {'package': u'runtime',
                             'type': u'Send',
                             'stream': '0',
                             'name': 'New operator'}}
        
        returned = self.operators.addData(data)
        
        self.assertEqual(2, len(self.model.operators))
        op = self.model.operators['1']
        
        self.assertTrue('1' in self.stream.operators)
        self.assertEqual(returned, op.data)
        self.assertEqual('1', op.data['operator']['id'])
        self.assertEqual('runtime', op.data['operator']['package'])
        self.assertEqual('Send', op.data['operator']['type'])
        self.assertEqual('none', op.data['operator']['status'])
        self.assertEqual('New operator', op.data['operator']['name'])
        self.assertEqual('0', op.data['operator']['stream'])
        self.assertEqual(2, len(self.model.operators))
        self.assertEqual(1, len(self.model.inputs))
        self.assertEqual(1, len(self.model.outputs))
        self.assertEqual(3, len(self.model.parameters))
        
    def testAddDataWhileActive(self):
        self.stromxStream.start()
        data = {'operator': {'package': u'runtime',
                             'type': u'Send',
                             'stream': '0',
                             'name': 'New operator'}}
        
        self.assertRaises(model.Failed, self.operators.addData, data)
        
        self.assertEqual(1, len(self.model.operators))
        self.assertEqual(1, len(self.errorSink.errors))
        
    def testAddDataInvalidOperator(self):
        data = {'operator': {'package': 'package',
                             'type': 'Invalid',
                             'stream': '0'}}
        
        self.assertRaises(model.Failed, self.operators.addData, data)
        
        self.assertEqual(1, len(self.model.operators))
        self.assertEqual(1, len(self.errorSink.errors))
        
    def testDataDeinitialized(self):
        kernel = stromx.runtime.Fork()
        stromxOp = self.stromxStream.addOperator(kernel)
        op = self.operators.addStromxOp(stromxOp, self.stream)
        
        data = {'operator': {'id': '1', 
                             'name': '',
                             'package': 'runtime',
                             'type': 'Fork',
                             'status': 'none',
                             'version': '0.8.0',
                             'parameters': ['3'],
                             'outputs': [],
                             'inputs': [],
                             'position': {'x': 0.0, 'y': 0.0} ,
                             'stream': '0'}}
        self.assertEqual(data, op.data)
    
    def testFindOperatorModel(self):
        op = self.operators.findOperatorModel(self.stromxOp)
        self.assertEqual(self.operator, op)
        
    def testSetNone(self):
        kernel = stromx.test.ParameterOperator()
        stromxOp = self.stromxStream.addOperator(kernel)
        self.stromxStream.initializeOperator(stromxOp)
        op = self.operators.addStromxOp(stromxOp, self.stream)
        
        self.operators.set('1', {'operator': 
                                 {'status': 'none'}
                                })
                                
        data = {'operator': {'id': '1', 
                             'name': '',
                             'package': 'test',
                             'type': 'ParameterOperator',
                             'status': 'none',
                             'version': '1.2.3',
                             'parameters': ['13'],
                             'outputs': [],
                             'inputs': [],
                             'position': {'x': 0.0, 'y': 0.0},
                             'stream': '0'}}
        self.assertEqual(data, op.data)         
        
    def testSetInitialized(self):
        kernel = stromx.test.ParameterOperator()
        stromxOp = self.stromxStream.addOperator(kernel)
        op = self.operators.addStromxOp(stromxOp, self.stream)
        
        self.operators.set('1', {'operator': 
                                 {'status': 'initialized'}
                                })
                                
        data = {'operator': {'id': '1', 
                             'name': '',
                             'package': 'test',
                             'type': 'ParameterOperator',
                             'status': 'initialized',
                             'version': '1.2.3',
                             'parameters': ['4', '5', '6', '7', '8', '9', '10',
                                            '11', '12', '13'],
                             'inputs': ['1', '2'],
                             'outputs': ['1', '2'],
                             'position': {'x': 0.0, 'y': 0.0},
                             'stream': '0'}}
        self.assertEqual(data, op.data)
        
    def testSetInitializedAlreadyInitialized(self):
        kernel = stromx.test.ParameterOperator()
        stromxOp = self.stromxStream.addOperator(kernel)
        self.stromxStream.initializeOperator(stromxOp)
        op = self.operators.addStromxOp(stromxOp, self.stream)
        
        self.operators.set('1', {'operator': 
                                 {'status': 'initialized'}
                                })
                                
        self.assertEqual('initialized', op.data['operator']['status'])
        
    def testSetInitializedFails(self):
        kernel = stromx.test.ExceptionOperator()
        stromxOp = self.stromxStream.addOperator(kernel)
        op = self.operators.addStromxOp(stromxOp, self.stream)
        stromxOp.setParameter(1, stromx.runtime.Bool(True))
        
        self.assertRaises(model.Failed, self.operators.set,
                          '1', {'operator': {'status': 'initialized'}})
                                
        self.assertEqual('none', op.data['operator']['status'])
        self.assertEqual([], op.data['operator']['inputs'])
        self.assertEqual([], op.data['operator']['outputs'])
        self.assertEqual(1, len(self.errorSink.errors))
        self.assertEqual('Failed to initialize operator.',
                         self.errorSink.errors[0].description)
        
    def testSetNoneAlreadyNone(self):
        kernel = stromx.test.ParameterOperator()
        stromxOp = self.stromxStream.addOperator(kernel)
        op = self.operators.addStromxOp(stromxOp, self.stream)
        
        self.operators.set('1', {'operator': {'status': 'none'}})
                                
        self.assertEqual('none', op.data['operator']['status'])  
        
    def testSetNoneFails(self):
        kernel = stromx.test.ExceptionOperator()
        stromxOp = self.stromxStream.addOperator(kernel)
        self.stromxStream.initializeOperator(stromxOp)
        stromxOp.setParameter(5, stromx.runtime.Bool(True))
        op = self.operators.addStromxOp(stromxOp, self.stream)
        
        self.operators.set('1', {'operator': 
                                 {'status': 'none'}
                                })
                                
        self.assertEqual('none', op.data['operator']['status'])
        self.assertEqual(1, len(self.errorSink.errors))
        self.assertEqual('Failed to deinitialize operator.',
                         self.errorSink.errors[0].description)    
        
    def testDelete(self):
        self.operators.delete('0')
        
        self.assertFalse(self.stromxOp in self.stromxStream.operators())
        self.assertFalse('5' in self.stream.operators)
        self.assertEqual(0, len(self.model.operators))
        self.assertEqual(0, len(self.model.inputs))
        self.assertEqual(0, len(self.model.outputs))
        self.assertEqual(0, len(self.model.parameters))    
        
    def testDeleteWhileActive(self):
        self.stromxStream.start()
          
        self.assertRaises(model.Failed, self.operators.delete, '0')
        
        self.assertEqual(1, len(self.model.operators))
        self.assertEqual(1, len(self.model.inputs))
        self.assertEqual(1, len(self.model.outputs))
        self.assertEqual(3, len(self.model.parameters)) 
        self.assertEqual(1, len(self.errorSink.errors))
        
    def tearDown(self):
        self.__stream = None
        
class ParametersTest(unittest.TestCase):
    def setUp(self):
        self.model = model.Model()
        self.errorSink = ErrorSink()
        self.model.errors.addHandler(self.errorSink.handleError)
        self.parameters = self.model.parameters
        
        fileModel = model.File("", self.model)
        self.stream = self.model.streams.addFile(fileModel)
        self.stromxStream = self.stream.stromxStream
        
        kernel = stromx.runtime.Receive()
        self.receive = self.stromxStream.addOperator(kernel)
        kernel = stromx.runtime.Fork()
        self.fork = self.stromxStream.addOperator(kernel)
        kernel = stromx.cvsupport.DummyCamera()
        self.dummyCamera = self.stromxStream.addOperator(kernel)
        kernel = stromx.test.ExceptionOperator()
        self.exceptionOperator = self.stromxStream.addOperator(kernel)
        kernel = stromx.test.ParameterOperator()
        self.parameterOperator = self.stromxStream.addOperator(kernel)
        self.stromxStream.initializeOperator(self.fork)
        self.stromxStream.initializeOperator(self.receive)
        self.stromxStream.initializeOperator(self.dummyCamera)
        self.stromxStream.initializeOperator(self.exceptionOperator)
        self.stromxStream.initializeOperator(self.parameterOperator)
        
    def testDataUrl(self):
        self.model.operators.addStromxOp(self.receive, self.stream)
        param = self.parameters['0']
        data = {'parameter': {'descriptions': [],
                              'id': '0',
                              'maximum': 0,
                              'minimum': 0,
                              'rows': 0,
                              'cols': 0,
                              'state': 'current',
                              'value': 'localhost',
                              'title': 'URL',
                              'variant': { 
                                'ident': 'string',
                                'title': 'String'
                              },
                              'operator': '0',
                              'access': 'inactive',
                              'behavior': 'persistent',
                              'currentType': 'parameter',
                              'originalType': 'parameter',
                              'observers': []}}
        self.assertEqual(data, param.data)
        
    def testSetUrl(self):
        self.model.operators.addStromxOp(self.receive, self.stream)
        param = self.parameters['0']
        param.set({'parameter': {'id': '0',
                                 'value': '127.0.0.1'}})
        self.assertEqual('127.0.0.1', self.receive.getParameter(1).get())
        
    def testSetUrlUnicode(self):
        self.model.operators.addStromxOp(self.receive, self.stream)
        param = self.parameters['0']
        param.set({'parameter': {'id': '0',
                                 'value': u'127.0.0.1'}})
        self.assertEqual('127.0.0.1', self.receive.getParameter(1).get())
        
    def testDataPort(self):
        self.model.operators.addStromxOp(self.receive, self.stream)
        param = self.parameters['1']
        data = {'parameter': {'descriptions': [],
                              'id': '1',
                              'maximum': 65535,
                              'minimum': 49152,
                              'rows': 0,
                              'cols': 0,
                              'value': 49152,
                              'state': 'current',
                              'title': 'TCP port',
                              'variant': { 
                                'ident': 'int',
                                'title': 'UInt16'
                              },
                              'operator': '0',
                              'access': 'inactive',
                              'behavior': 'persistent',
                              'currentType': 'parameter',
                              'originalType': 'parameter',
                              'observers': []}}
        self.assertEqual(data, param.data)
        
    def testDataImage(self):
        self.model.operators.addStromxOp(self.dummyCamera, self.stream)
        param = self.parameters['10']
        data = param.data['parameter']
        
        self.assertEqual({'width': 0, 'height': 0}, data['value'])
        self.assertEqual('image', data['variant']['ident'])
        
    def testSetImage(self):
        self.model.operators.addStromxOp(self.dummyCamera, self.stream)
        param = self.parameters['10']
        
        param.set({'parameter': {'id': '10',
                                 'value': {'values': _colorImage}}})
        
        data = param.data['parameter']['value']
        self.assertEqual({'width': 12, 'height': 13}, data) 
        
    def testSetPort(self):
        self.model.operators.addStromxOp(self.receive, self.stream)
        param = self.parameters['1']
        param.set({'parameter': {'id': '0',
                                 'value': 50000}})
        self.assertEqual(50000, self.receive.getParameter(2).get())
        
    def testSetNone(self):
        self.model.operators.addStromxOp(self.receive, self.stream)
        param = self.parameters['1']
        param.set({'parameter': {'id': '0',
                                 'value': None}})
        self.assertEqual(49152, self.receive.getParameter(2).get())
        
    def testDataNumberOfOutputs(self):
        self.model.operators.addStromxOp(self.fork, self.stream)
        param = self.parameters['0']
        data = {'parameter': {'descriptions': [],
                              'id': '0',
                              'maximum': 4,
                              'minimum': 2,
                              'rows': 0,
                              'cols': 0,
                              'value': 2,
                              'state': 'current',
                              'title': 'Number of outputs',
                              'variant': { 
                                'ident': 'int',
                                'title': 'UInt32'
                              },
                              'operator': '0',
                              'access': 'none',
                              'behavior': 'persistent',
                              'currentType': 'parameter',
                              'originalType': 'parameter',
                              'observers': []}}
        self.assertEqual(data, param.data)
        
    def testDataMatrixParameter(self):
        self.model.operators.addStromxOp(self.parameterOperator, self.stream)
        param = self.parameters['4']
        data = {'parameter': {'descriptions': [],
                              'id': '4',
                              'maximum': 0,
                              'minimum': 0,
                              'rows': 0,
                              'cols': 0,
                              'value': {
                                  'rows': 3,
                                  'cols': 4,
                                  'values': [
                                      [0.0, 1.0, 2.0, 3.0],
                                      [1.0, 2.0, 3.0, 4.0],
                                      [2.0, 3.0, 4.0, 5.0]
                                  ]
                              },
                              'state': 'current',
                              'title': 'Matrix parameter',
                              'variant': { 
                                'ident': 'matrix',
                                'title': 'Float32 matrix'
                              },
                              'operator': '0',
                              'access': 'inactive',
                              'behavior': 'persistent',
                              'currentType': 'parameter',
                              'originalType': 'parameter',
                              'observers': []}}
        self.assertEqual(data, param.data)
        
    def testSetMatrix(self):
        self.model.operators.addStromxOp(self.parameterOperator, self.stream)
        param = self.parameters['4']
        
        param.set({'parameter': {'id': '10',
                                 'value': {
                                    'rows': 1,
                                    'cols': 2,
                                    'values': [[1.2, '3.4']]
                                  }
                                }})
        
        data = param.data['parameter']['value']
        self.assertEqual(1, data['rows']) 
        self.assertEqual(2, data['cols']) 
        self.assertAlmostEqual(1.2, data['values'][0][0], places = 3) 
        self.assertAlmostEqual(3.4, data['values'][0][1], places = 3) 
        
    def testSetNumberOfOutputs(self):
        self.model.operators.addStromxOp(self.fork, self.stream)
        self.stromxStream.deinitializeOperator(self.fork)
        param = self.parameters['0']
        param.set({'parameter': {'id': '0',
                                 'value': 3}})
        self.assertEqual(3, self.fork.getParameter(1).get())
        
    def testDataPixelType(self):
        self.model.operators.addStromxOp(self.dummyCamera, self.stream)
        param = self.parameters['1']
        data = {'parameter': {'descriptions': ['0', '1', '2'],
                              'id': '1',
                              'maximum': 0,
                              'minimum': 0,
                              'rows': 0,
                              'cols': 0,
                              'value': 0,
                              'state': 'current',
                              'title': 'Trigger mode',
                              'variant': { 
                                'ident': 'enum',
                                'title': 'Enum'
                              },
                              'operator': '0',
                              'access': 'full',
                              'behavior': 'persistent',
                              'currentType': 'parameter',
                              'originalType': 'parameter',
                              'observers': []}}
        self.assertEqual(data, param.data)
        
    def testSetPixelType(self):
        self.model.operators.addStromxOp(self.dummyCamera, self.stream)
        param = self.parameters['1']
        param.set({'parameter': {'id': '1',
                                 'value': 1}})
        self.assertEqual(1, self.dummyCamera.getParameter(4).get())
        
    def testSetPixelTypeZero(self):
        self.model.operators.addStromxOp(self.dummyCamera, self.stream)
        param = self.parameters['1']
        param.set({'parameter': {'id': '1',
                                 'value': 1}})
        param.set({'parameter': {'id': '1',
                                 'value': 0}})
        self.assertEqual(0, self.dummyCamera.getParameter(4).get())
        
    def testDataException(self):
        self.__activateExceptionOnParameter()
        param = self.parameters['6']
        
        state = param.data['parameter']['state']
        self.assertEqual('accessFailed', state)
        self.assertEqual(1, len(self.errorSink.errors))
        
    def testSetParameterException(self):
        self.__activateExceptionOnParameter()
        param = self.parameters['6']
        
        self.assertRaises(model.Failed, param.set, 
                          {'parameter': {'id': '0', 'value': 1}})
        state = param.data['parameter']['state']
        self.assertEqual('accessFailed', state)
        self.assertEqual(2, len(self.errorSink.errors))
        
    def testDataTrigger(self):
        self.model.operators.addStromxOp(self.parameterOperator, self.stream)
        valueParam = self.parameters['6']
        param = self.parameters['7']
        
        self.assertEqual('trigger', param.data['parameter']['variant']['ident'])
        self.assertEqual('push', param.data['parameter']['behavior'])
        self.assertEqual(0, valueParam.data['parameter']['value'])
        
    def testDataPushParameter(self):
        self.model.operators.addStromxOp(self.parameterOperator, self.stream)
        param = self.parameters['8']
        
        self.assertEqual('push', param.data['parameter']['behavior'])
        self.assertEqual(0, len(self.errorSink.errors))
        self.assertEqual(None, param.data['parameter']['value'])
        
    def testDataPullParameter(self):
        self.model.operators.addStromxOp(self.parameterOperator, self.stream)
        param = self.parameters['9']
        
        self.assertEqual('pull', param.data['parameter']['behavior'])
        self.assertEqual(0, len(self.errorSink.errors))
        self.assertEqual(3.0, param.data['parameter']['value'])
        
    def testSetDataPullParameter(self):
        self.model.operators.addStromxOp(self.parameterOperator, self.stream)
        param = self.parameters['9']
        
        param.set({'parameter': {'id': '9',
                                 'value': 1.3}})
        
        self.assertEqual(0, len(self.errorSink.errors))
        self.assertEqual(3.0, param.data['parameter']['value'])
        
    def testSetTrigger(self):
        self.model.operators.addStromxOp(self.parameterOperator, self.stream)
        valueParam = self.parameters['6']
        param = self.parameters['7']
        
        param.set({'parameter': {'id': '7',
                                 'value': 1}})
        self.assertEqual(1, valueParam.data['parameter']['value'])
        
    def testSetBool(self):
        self.stromxStream.deinitializeOperator(self.dummyCamera)
        self.model.operators.addStromxOp(self.dummyCamera, self.stream)
        param = self.parameters['0']
        
        param.set({'parameter': {'id': '7',
                                 'value': True}})
        self.assertEqual(True, param.data['parameter']['value'])
        
    def testTypeInput(self):
        op = self.model.operators.addStromxOp(self.fork, self.stream)
        connector = self.model.inputs['0']
        connector.set({'input': {'currentType': 'parameter',
                                 'behavior': 'push'}})
        param = self.model.parameters['1']
        param.set({'parameter': {'currentType': 'input'}})
        
        self.assertFalse(self.model.parameters.has_key('1'))
        self.assertTrue(self.model.inputs.has_key('1'))
        self.assertTrue(op.data['operator']['inputs'].count('1'))
        
    def testTypeParameter(self):
        op = self.model.operators.addStromxOp(self.fork, self.stream)
        connector = self.model.inputs['0']
        connector.set({'input': {'currentType': 'parameter',
                                 'behavior': 'push'}})
        param = self.model.parameters['1']
        param.set({'parameter': {'currentType': 'parameter'}})
        
        self.assertTrue(self.model.parameters.has_key('1'))
        self.assertTrue(op.data['operator']['parameters'].count('1'))
        self.assertTrue('push', param.data['parameter']['behavior'])
        
    def testBehavior(self):
        self.model.operators.addStromxOp(self.fork, self.stream)
        connector = self.model.inputs['0']
        connector.set({'input': {'currentType': 'parameter',
                                 'behavior': 'push'}})
        param = self.model.parameters['1']
        self.assertEqual('push', param.data['parameter']['behavior'])
        
        param.set({'parameter': {'currentType': 'parameter',
                                 'behavior': 'persistent'}})
        self.assertEqual('persistent', param.data['parameter']['behavior'])
        
    def testTypeOutput(self):
        op = self.model.operators.addStromxOp(self.fork, self.stream)
        connector = self.model.outputs['0']
        connector.set({'output': {'currentType': 'parameter',
                                  'behavior': 'persistent'}})
        param = self.model.parameters['1']
        param.set({'parameter': {'currentType': 'output'}})
        
        self.assertFalse(self.model.parameters.has_key('1'))
        self.assertTrue(self.model.outputs.has_key('1'))
        self.assertTrue(op.data['operator']['outputs'].count('1'))
        
    def testSetTypeOutputInput(self):
        self.model.operators.addStromxOp(self.fork, self.stream)
        connector = self.model.inputs['0']
        connector.set({'input': {'currentType': 'parameter',
                                 'behavior': 'push'}})
        param = self.model.parameters['1']
        
        self.assertRaises(model.Failed, param.set,
                          {'parameter': {'currentType': 'output'}})
        self.assertEqual(1, len(self.errorSink.errors))
        self.assertTrue(self.model.parameters.has_key('1'))
        
    def testDelete(self):
        # create some parameters
        self.model.operators.addStromxOp(self.receive, self.stream)
        
        # create a view and add an observer
        self.model.views.addData({'view': {'stream': '0'}})
        self.model.parameterObservers.addData(
            {'parameterObserver': {'parameter': '0', 'view': '0'}}
        )
        
        self.model.parameters.delete('0')
        
        self.assertFalse(self.model.parameters.has_key('0'))
        self.assertFalse(self.model.parameterObservers.has_key('0'))
        self.assertFalse('0' in self.model.views['0'].observers)
        
    def __activateExceptionOnParameter(self):
        self.model.operators.addStromxOp(self.exceptionOperator, self.stream)
        param = self.parameters['5']
        param.set({'parameter': {'id': '0',
                                 'value': 1}})
        
class EnumDescriptionsTest(unittest.TestCase):
    def setUp(self):
        self.model = model.Model()
        self.enumDescriptions = self.model.enumDescriptions
        
        self.stream = stromx.runtime.Stream()
        kernel = stromx.cvsupport.DummyCamera()
        dummyCamera = self.stream.addOperator(kernel)
        self.stream.initializeOperator(dummyCamera)
        pixelType = dummyCamera.info().parameters()[1]
        self.manual = pixelType.descriptions()[0]
        
    def testData(self):
        desc = self.enumDescriptions.addStromxEnumDescription(self.manual)
        data = {'enumDescription': {'id': '0', 
                                    'title': 'Software trigger', 
                                    'value': 0}}
        self.assertEqual(data, desc.data)
        
class ConnectionsTest(unittest.TestCase):
    def setUp(self):
        self.model = model.Model()
        self.errorSink = ErrorSink()
        self.model.errors.addHandler(self.errorSink.handleError)
        self.connections = self.model.connections
        
        fileModel = model.File("", self.model)
        self.stream = self.model.streams.addFile(fileModel)
        self.stromxStream = self.stream.stromxStream
        
        kernel = stromx.runtime.Fork()
        stromxFork = self.stromxStream.addOperator(kernel)
        kernel = stromx.runtime.Block()
        stromxReceive = self.stromxStream.addOperator(kernel)
        
        self.stromxStream.initializeOperator(stromxFork)
        self.stromxStream.initializeOperator(stromxReceive)
        
        self.fork = self.model.operators.addStromxOp(stromxFork, self.stream)
        self.receive = self.model.operators.addStromxOp(stromxReceive, 
                                                        self.stream)
        
    def testData(self):
        source = self.model.outputs['2']
        target = self.model.inputs['0']
        connection = self.connections.addConnection(self.stream, source, target)
        
        data = {'connection': {'id': '0',
                               'thread': None,
                               'output': '2', 
                               'input': '0', 
                               'stream': '0'}}
        self.assertEqual(data, connection.data)
        
        self.assertEqual(['0'], source.data['output']['connections'])
        self.assertEqual('0', target.data['input']['connection'])
        
    def testAddData(self):
        newData = {'connection': {'output': '2', 
                                  'input': '0'}}
                               
        returned = self.model.connections.addData(newData)
        
        output = self.stromxStream.connectionSource(self.fork.stromxOp, 0)
        self.assertEqual(output.op(), self.receive.stromxOp)
        self.assertEqual(output.id(), 2)
        
        self.assertEqual(['0'], self.model.streams['0'].connections)
        
        data = self.model.connections['0'].data
        self.assertEqual(returned, data)
        self.assertEqual('0', data['connection']['id'])
        self.assertEqual('2', data['connection']['output'])
        self.assertEqual('0', data['connection']['input'])
        
    def testAddDataInputConnected(self):
        newData = {'connection': {'output': '2', 
                                  'input': '0'}}
        self.model.connections.addData(newData)
        
        self.assertRaises(model.Failed, self.model.connections.addData,
                          newData)
        self.assertEqual(1, len(self.errorSink.errors))
        
    def testAddDataWhileActive(self):
        self.stromxStream.start()
        newData = {'connection': {'output': '2', 
                                  'input': '0'}}
                               
        self.assertRaises(model.Failed, self.model.connections.addData,
                          newData)
        self.assertEqual(0, len(self.model.connections))
        self.assertEqual(1, len(self.errorSink.errors))
        
    def testSetStromxThreadId(self):
        newData = {'connection': {'output': '2', 
                                  'input': '0'}}
        self.model.connections.addData(newData)
        
        self.model.connections['0'].setStromxThreadId(10)
        
        data = self.model.connections['0'].data
        self.assertEqual(10, data['connection']['thread'])
        
    def testDelete(self):
        newData = {'connection': {'output': '2', 
                                  'input': '0'}}
        self.model.connections.addData(newData)
        
        source = self.model.outputs['2']
        target = self.model.inputs['0']
        self.model.connections.delete('0')
        
        self.assertEqual([], source.data['output']['connections'])
        self.assertEqual(None, target.data['input']['connection'])
        self.assertEqual([], self.stream.connections)
        
        output = self.stromxStream.connectionSource(self.fork.stromxOp, 0)
        self.assertFalse(output.valid())
        
    def testDeleteWileActive(self):
        newData = {'connection': {'output': '2', 
                                  'input': '0'}}
        self.model.connections.addData(newData)
        self.stromxStream.start()
        
        self.assertRaises(model.Failed, self.model.connections.delete, '0')
        
        self.assertEqual(1, len(self.errorSink.errors))
        self.assertEqual(1, len(self.model.connections))
        
    def testDeleteWhileActive(self):
        newData = {'connection': {'thread': '0',
                                  'output': '2', 
                                  'input': '0'}}
        self.model.connections.addData(newData)
        self.stromxStream.start()
        
        self.assertRaises(model.Failed, self.model.connections.delete,
                          '0')
        self.assertEqual(1, len(self.errorSink.errors))
        
class InputsTest(unittest.TestCase):
    def setUp(self):
        self.model = model.Model()
        self.errorSink = ErrorSink()
        self.model.errors.addHandler(self.errorSink.handleError)
        
        fileModel = model.File("", self.model)
        self.stream = self.model.streams.addFile(fileModel)
        self.stromxStream = self.stream.stromxStream
        
        kernel = stromx.runtime.Fork()
        stromxOp = self.stromxStream.addOperator(kernel)
        self.stromxStream.initializeOperator(stromxOp)
        self.model.operators.addStromxOp(stromxOp, self.stream)
        
    def testData(self):
        connector = self.model.inputs['0']
        data = {'input': {'id': '0',
                          'operator': '0',
                          'title': 'Input',
                          'observers': [],
                          'connection': None,
                          'behavior': 'persistent',
                          'currentType': 'input',
                          'variant': { 'ident': 'none', 'title': 'Data' }}}
        self.assertEqual(data, connector.data)
        
    def testSetTypePushParameter(self):
        connector = self.model.inputs['0']
        connector.set({'input': {'currentType': 'parameter',
                                 'behavior': 'push'}})
        
        self.assertFalse(self.model.inputs.has_key('0'))
        param = self.model.parameters['1']
        self.assertEqual('input', param.data['parameter']['originalType'])
        self.assertEqual('parameter', param.data['parameter']['currentType'])
        self.assertEqual('push', param.data['parameter']['behavior'])
        
    def testSetTypeStreamActive(self):
        self.stream.active = True
        connector = self.model.inputs['0']
        
        self.assertRaises(model.Failed, connector.set, 
                          {'input': {'currentType': 'parameter',
                                     'behavior': 'persistent'}})
        self.assertEqual(1, len(self.errorSink.errors))
        self.assertTrue(self.model.inputs.has_key('0'))
        self.assertFalse(self.model.parameters.has_key('1'))
        
    def testSetTypeInput(self):
        self.stream.active = True
        connector = self.model.inputs['0']
        
        connector.set({'input': {'currentType': 'input'}})
        self.assertTrue(self.model.inputs.has_key('0'))
        
    def testSetTypePullParameter(self):
        connector = self.model.inputs['0']
        
        self.assertRaises(model.Failed, connector.set, 
                          {'input': {'currentType': 'parameter', 
                                     'behavior': 'pull'}})
        self.assertEqual(1, len(self.errorSink.errors))
        self.assertTrue(self.model.inputs.has_key('0'))
        self.assertFalse(self.model.parameters.has_key('1'))
        
    def testSetTypePersistentParameter(self):
        connector = self.model.inputs['0']
        connector.set({'input': {'currentType': 'parameter',
                                 'behavior': 'persistent'}})
        
        self.assertFalse(self.model.inputs.has_key('0'))
        param = self.model.parameters['1']
        self.assertEqual('input', param.data['parameter']['originalType'])
        self.assertEqual('parameter', param.data['parameter']['currentType'])
        self.assertEqual('persistent', param.data['parameter']['behavior'])
        
    def testDelete(self):
        # create a connection
        source = self.model.outputs['0']
        target = self.model.inputs['0']
        self.model.connections.addConnection(self.stream, source, target)
        
        # create a view and add an observer
        self.model.views.addData({'view': {'stream': '0'}})
        self.model.inputObservers.addData(
            {'inputObserver': {'input': '0', 'view': '0'}}
        )
        
        self.model.inputs.delete('0')
        
        self.assertFalse(self.model.inputs.has_key('0'))
        self.assertFalse(self.model.inputObservers.has_key('0'))
        self.assertFalse('0' in self.model.views['0'].observers)
        self.assertEqual(dict(), self.model.connections)
        
class OutputsTest(unittest.TestCase):
    def setUp(self):
        self.model = model.Model()
        
        fileModel = model.File("", self.model)
        self.stream = self.model.streams.addFile(fileModel)
        self.stromxStream = self.stream.stromxStream
        
        kernel = stromx.runtime.Fork()
        stromxOp = self.stromxStream.addOperator(kernel)
        self.stromxStream.initializeOperator(stromxOp)
        self.model.operators.addStromxOp(stromxOp, self.stream)
        
    def testData(self):
        connector = self.model.outputs['1']
        data = {'output': {'id': '1',
                           'operator': '0',
                           'title': 'Output 1',
                           'behavior': 'persistent',
                           'currentType': 'output',
                           'observers': [],
                           'connections': [],
                           'variant': { 'ident': 'none', 'title': 'Data' }}}
        self.assertEqual(data, connector.data)
        
    def testSetTypePullParameter(self):
        connector = self.model.outputs['1']
        connector.set({'output': {'currentType': 'parameter',
                                  'behavior': 'pull'}})
        
        self.assertFalse(self.model.outputs.has_key('1'))
        param = self.model.parameters['1']
        self.assertEqual('parameter', param.data['parameter']['currentType'])
        self.assertEqual('output', param.data['parameter']['originalType'])
        self.assertEqual('pull', param.data['parameter']['behavior'])
        
    def testSetTypePersistentParameter(self):
        connector = self.model.outputs['1']
        connector.set({'output': {'currentType': 'parameter',
                                  'behavior': 'persistent'}})
        
        self.assertFalse(self.model.outputs.has_key('1'))
        param = self.model.parameters['1']
        self.assertEqual('parameter', param.data['parameter']['currentType'])
        self.assertEqual('output', param.data['parameter']['originalType'])
        self.assertEqual('persistent', param.data['parameter']['behavior'])
        
    def testDelete(self):
        # create a connection
        source = self.model.outputs['0']
        target = self.model.inputs['0']
        self.model.connections.addConnection(self.stream, source, target)
        
        # create a view and add an observer
        self.model.views.addData({'view': {'stream': '0'}})
        self.model.outputObservers.addData(
            {'outputObserver': {'output': '0', 'view': '0'}}
        )
        
        self.model.outputs.delete('0')
        
        self.assertFalse(self.model.outputs.has_key('0'))
        self.assertFalse(self.model.outputObservers.has_key('0'))
        self.assertFalse('0' in self.model.views['0'].observers)
        self.assertEqual(dict(), self.model.connections)
    
class ViewsTest(unittest.TestCase):
    def setUp(self):
        shutil.rmtree('temp', True)
        self.model = None
        
    def setupViewData(self):
        shutil.copytree('data/views', 'temp')
        
        self.model = model.Model('temp', _packages)
        self.streamFile = self.model.files['0']
        self.model.streams.addFile(self.streamFile)
        
    def testAddData(self):
        shutil.copytree('data/stream', 'temp')
        self.model = model.Model('temp', _packages)
        stream = self.model.streams.addFile(self.model.files['0'])
        viewData = {'view': {'name': 'View name',
                             'observers': [],
                             'stream': '0'}}
        
        returned = self.model.views.addData(viewData)
        
        refData = {'view': {'id': '0',
                            'name': 'View name',
                            'observers': [],
                            'stream': '0'}}
        self.assertEqual(refData, returned)
        self.assertEqual(refData, self.model.views['0'].data)
        self.assertEqual(['0'], stream.views)
        
    def testData(self):
        self.setupViewData()
        streamFile = self.model.files['1']
        self.model.streams.addFile(streamFile)
        
        data = {'view': {'id': '1',
                         'name': 'View name',
                         'observers': [{'id': '0', 'type': 'parameterObserver'},
                                       {'id': '0', 'type': 'inputObserver'},
                                       {'id': '0', 'type': 'outputObserver'}],
                         'stream': '1'}}
        self.assertEqual(data, self.model.views['1'].data)
        
    def testDelete(self):
        self.setupViewData()
        stream = self.model.streams['0']
        
        self.model.views.delete('0')
        
        self.assertEqual({}, self.model.views)
        self.assertEqual([], stream.views)
        
    def testDeleteStreamWithView(self):
        self.setupViewData()
        streamFile = self.model.files['1']
        stream = self.model.streams.addFile(streamFile)
        
        self.model.streams.delete(stream.index)
        self.assertEqual(1, len(self.model.views))
        self.assertEqual(0, len(self.model.inputObservers))
        self.assertEqual(0, len(self.model.parameterObservers))
        self.assertEqual(0, len(self.model.connectorValues))
        
    def testSetName(self):
        self.setupViewData()
        
        view = self.model.views['0']
        view.set({'view': {'id': '0',
                           'name': 'New name'}})
        self.assertEqual('New name', view.name)
        
    def tearDown(self):
        shutil.rmtree('temp', True)
        
class ObserversTest(unittest.TestCase):
    def setUp(self):
        shutil.rmtree('temp', True)
        shutil.copytree('data/views', 'temp')
        
        self.model = model.Model('temp', _packages)
        self.streamFile = self.model.files['1']
        self.model.streams.addFile(self.streamFile)
        
        self.observer = self.model.inputObservers['0']
        self.stromxObserver = self.observer.stromxObserver
        
    def testSetVisualization(self):
        self.observer.set({'inputObserver': {'id': '0',
                                             'visualization': 'lines'}})
        self.assertEqual('lines', self.stromxObserver.visualization)
        
    def testSetProperties(self):
        properties = {'color': '#ff00ff'}
        self.observer.set({'inputObserver': {'id': '0',
                                             'properties': properties
                                            }})
        self.assertEqual('#ff00ff', self.stromxObserver.properties['color'])
        
    def testSetActive(self):
        self.observer.set({'inputObserver': {'id': '0',
                                             'active': False}})
        self.assertEqual(False, self.stromxObserver.active)
        
    def tearDown(self):
        shutil.rmtree('temp', True)
        
class ParameterObserversTest(unittest.TestCase):
    def setUp(self):
        shutil.rmtree('temp', True)
        shutil.copytree('data/views', 'temp')
        self.model = model.Model('temp', _packages)
        
    def setupView(self):
        streamFile = self.model.files['1']
        self.model.streams.addFile(streamFile)
        
    def testAddData(self):
        streamFile = self.model.files['0']
        self.model.streams.addFile(streamFile)
        data = {'parameterObserver': {'id': '0',
                                      'parameter': '2',
                                      'view': '0'}}
        
        returned = self.model.parameterObservers.addData(data)
        
        refData = {'parameterObserver': {'id': '0',
                                         'parameter': '2',
                                         'view': '0',
                                         'active': True,
                                         'properties': {},
                                         'visualization': 'value',
                                         'visualizations': ['value', 'none'],
                                         'zvalue': 0}}
        self.assertEqual(refData, returned)
        self.assertEqual(refData, self.model.parameterObservers['0'].data)
        viewModel = self.model.views['0']
        self.assertEqual([{'id': '0', 'type': 'parameterObserver'}],
                         viewModel.observers)
        self.assertEqual(['0'], self.model.parameters['2'].observers);
        
    def testDelete(self):
        self.setupView()
        viewModel = self.model.views['0']
        stromxView = viewModel.stromxView
        
        self.model.parameterObservers.delete('0')
        
        self.assertEqual(2, len(viewModel.observers))
        self.assertEqual(2, len(stromxView.observers))
        self.assertEqual([], self.model.parameters['2'].observers)
        
    def tearDown(self):
        shutil.rmtree('temp', True)
        
class ConnectorObserversTestBase(unittest.TestCase):
    def setUp(self):
        shutil.rmtree('temp', True)
        shutil.copytree('data/views', 'temp')
        self.model = model.Model('temp', _packages)
        
    def setupEmptyView(self):
        streamFile = self.model.files['0']
        self.model.streams.addFile(streamFile)
        
    def setupView(self):
        streamFile = self.model.files['1']
        self.model.streams.addFile(streamFile)
        
    def tearDown(self):
        shutil.rmtree('temp', True)
        
class InputObserversTest(ConnectorObserversTestBase):        
    def testAddData(self):
        self.setupEmptyView()
        data = {'inputObserver': {'id': '0',
                                  'input': '2',
                                  'properties': {'color': '#00ff00'},
                                  'view': '0'}}
        
        returned = self.model.inputObservers.addData(data)
        
        refData = {'inputObserver': {'id': '0',
                                     'input': '2',
                                     'view': '0',
                                     'active': True,
                                     'value': '0',
                                     'properties': {'color': '#00ff00'},
                                     'visualization': 'value',
                                     'visualizations': ['value', 'none'],
                                     'zvalue': 0}}
        self.assertEqual(refData, returned)
        self.assertEqual(refData, self.model.inputObservers['0'].data)
        viewModel = self.model.views['0']
        self.assertEqual([{'id': '0', 'type': 'inputObserver'}],
                         viewModel.observers)
        refData = {'connectorValues': [{'variant': {'ident': 'none'},
                                        'id': '0',
                                        'value': None
                                        }]
                  }
        self.assertEqual(refData, self.model.connectorValues.data)
        self.assertEqual(['0'], self.model.inputs['2'].observers)
        
    def testDelete(self):
        self.setupView()
        viewModel = self.model.views['0']
        stromxView = viewModel.stromxView
        
        self.model.inputObservers.delete('0')
        
        self.assertEqual(2, len(viewModel.observers))
        self.assertEqual(2, len(stromxView.observers))
        self.assertEqual([], self.model.inputs['2'].observers)
        
class OutputObserversTest(ConnectorObserversTestBase):        
    def testAddData(self):
        self.setupEmptyView()
        data = {'outputObserver': {'id': '0',
                                   'output': '0',
                                   'properties': {'color': '#00ff00'},
                                   'view': '0'}}
        
        returned = self.model.outputObservers.addData(data)
        
        refData = {'outputObserver': {'id': '0',
                                      'output': '0',
                                      'view': '0',
                                      'active': True,
                                      'value': '0',
                                      'properties': {'color': '#00ff00'},
                                      'visualization': 'value',
                                      'visualizations': ['value', 'none'],
                                      'zvalue': 0}}
        self.assertEqual(refData, returned)
        self.assertEqual(refData, self.model.outputObservers['0'].data)
        viewModel = self.model.views['0']
        self.assertEqual([{'id': '0', 'type': 'outputObserver'}],
                         viewModel.observers)
        refData = {'connectorValues': [{'variant': {'ident': 'none'},
                                        'id': '0',
                                        'value': None
                                        }]
                  }
        self.assertEqual(refData, self.model.connectorValues.data)
        self.assertEqual(['0'], self.model.outputs['0'].observers)
        
    def testDelete(self):
        self.setupView()
        viewModel = self.model.views['0']
        stromxView = viewModel.stromxView
        
        self.model.outputObservers.delete('0')
        
        self.assertEqual(2, len(viewModel.observers))
        self.assertEqual(2, len(stromxView.observers))
        self.assertEqual([], self.model.outputs['2'].observers)
        
class ConnectorValuesTest(unittest.TestCase):
    def setUp(self):
        shutil.rmtree('temp', True)
        shutil.copytree('data/views', 'temp')
        
        self.model = model.Model('temp', _packages)
        
        observerFile = self.model.files['1']
        self.observerStream = self.model.streams.addFile(observerFile)
        
        cameraFile = self.model.files['2']
        self.cameraStream = self.model.streams.addFile(cameraFile)
        
        testDataFile = self.model.files['3']
        self.testDataStream = self.model.streams.addFile(testDataFile)
        
        # observer output connector
        outputFile = self.model.files['4']
        self.outputStream = self.model.streams.addFile(outputFile)
        
        # observer input connector
        inputFile = self.model.files['5']
        self.inputStream = self.model.streams.addFile(inputFile)
        
        self.data = None
        
    def setValue(self, value):
        self.data = value.data
        
    def testData(self):
        refData = {'connectorValue': {'id': '0', 
                                      'value': None, 
                                      'variant': {'ident': 'none'}}}
        self.assertEqual(refData, self.model.connectorValues['0'].data)
        
    def testHandlerInput(self):
        self.model.connectorValues.addHandler(self.setValue)
        self.inputStream.active = True
        time.sleep(0.5)
        self.inputStream.active = False
        
        self.assertEqual('int', self.data['connectorValue']['variant']['ident'])
        self.assertTrue(isinstance(self.data['connectorValue']['value'], int))
        
    def testHandlerOutput(self):
        self.model.connectorValues.addHandler(self.setValue)
        self.outputStream.active = True
        time.sleep(0.3)
        self.outputStream.active = False
        
        self.assertEqual('int', self.data['connectorValue']['variant']['ident'])
        self.assertTrue(isinstance(self.data['connectorValue']['value'], int))
        
    def testHandlerCamera(self):
        self.model.connectorValues.addHandler(self.setValue)
        self.cameraStream.active = True
        time.sleep(0.2)
        self.cameraStream.active = False
        
        self.assertEqual('image',
                         self.data['connectorValue']['variant']['ident'])
        value = self.data['connectorValue']['value']
        self.assertEqual(125, value['width'])
        self.assertEqual(128, value['height'])
        self.assertEqual('data:image/jpg;base64,/9j/4AAQ', value['values'][:30])
        self.assertEqual('oL/8QAtRAAAgEDAwIEAwUFBAQAAAF9', 
                         value['values'][200:230])
        
    def testHandlerLines(self):
        self.model.connectorValues.addHandler(self.setValue)
        self.testDataStream.active = True
        time.sleep(0.1)
        self.testDataStream.active = False
        
        self.assertEqual('matrix',
                         self.data['connectorValue']['variant']['ident'])
        value = self.data['connectorValue']['value']
        self.assertEqual(20, value['rows'])
        self.assertEqual(4, value['cols'])
        self.assertEqual([[100.0, 0.0, 100.0, 50.0], [150.0, 0.0, 150.0, 50.0]],
                         value['values'][2:4])
        
    def testHandlerPolygons(self):
        self.model.connectorValues.addHandler(self.setValue)
        opIndex = self.testDataStream.operators[1]
        op = self.model.operators[opIndex]
        
        DATA_TYPE = 0
        MATRIX_FLOAT_32 = 5
        OBJECT_TYPE = 1
        POLYGONS = 4
        paramIndex = op.parameters[OBJECT_TYPE]
        param = self.model.parameters[paramIndex]
        param.value = POLYGONS;
        paramIndex = op.parameters[DATA_TYPE]
        param = self.model.parameters[paramIndex]
        param.value = MATRIX_FLOAT_32;
        
        self.testDataStream.active = True
        time.sleep(0.2)
        self.testDataStream.active = False
        
        self.assertEqual('list',
                         self.data['connectorValue']['variant']['ident'])
        value = self.data['connectorValue']['value']
        self.assertEqual(6, value['numItems'])
        
    def tearDown(self):
        shutil.rmtree('temp', True)
    
class ErrorsTest(unittest.TestCase):
    def setUp(self):
        self.lastError = None
        self.errors = model.Errors()
        
    def storeError(self, error):
        self.lastError = error
        
    def testAddData(self):
        self.errors.addHandler(self.storeError)
        self.errors.addError('An error happened')
        self.assertEqual('An error happened',
                         self.lastError.data['error']['description'])
        
if __name__ == '__main__':
    unittest.main()