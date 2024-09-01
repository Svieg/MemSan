#TODO write a description for this script
#@author Chengbin, MyriaCore
#@category Functions
#@keybinding 
#@menupath 
#@toolbar 


#TODO Add User Code Here

# reference https://github.com/NationalSecurityAgency/ghidra/issues/826
from __future__ import division
import logging
import site
import sys
import os

from ghidra.program.model.block import BasicBlockModel
from ghidra.program.model.block import CodeBlockIterator
from ghidra.program.model.block import CodeBlockReference 
from ghidra.program.model.block import CodeBlockReferenceIterator 
from ghidra.program.model.listing import CodeUnitIterator;
from ghidra.program.model.listing import Function;
from ghidra.program.model.listing import FunctionManager;
from ghidra.program.model.listing import Listing;
from ghidra.program.database.code import InstructionDB

def addBB(bb, G, bb_func_map):
    listing = currentProgram.getListing();
    # iter over the instructions
    codeUnits = listing.getCodeUnits(bb, True)
    lastInstStart = 0x0
    lastInstEnd = 0x0

    bb_tbl_rows = ''
    i = 0
    while codeUnits.hasNext():
        codeUnit = codeUnits.next()
        # check if the code unit is the instruction
        if not isinstance(codeUnit, InstructionDB):
            continue
        # Record address of first instruction
        if i == 0:
            firstInstStart = codeUnit.getAddress().getOffset()

        lastInstStart = codeUnit.getAddress().getOffset()
        lastInstEnd = lastInstStart + codeUnit.getLength()

        bb_tbl_rows += ('''\t<TR><TD>%x:%s</TD></TR>\n''' % (lastInstStart, str(codeUnit)))
        i += 1 # Bump Counter

    bb_tbl_node = ('''  bb_%x [shape=plaintext label=<
    <TABLE BORDER="1" CELLBORDER="0" CELLSPACING="0">%s
    </TABLE>>];\n''' % (bb.getMinAddress().getOffset(), bb_tbl_rows))

    bb_func_map[bb.getMinAddress().getOffset()] = \
        'bb_%x' % (bb.getMinAddress().getOffset())

    # add node
    G += bb_tbl_node

    return G

def addSuccessors(bb_func_set, bb_func_map, G):


    listing = currentProgram.getListing();
    for bb in bb_func_set:
        codeUnits = listing.getCodeUnits(bb, True)
        lastInstStart = 0x0
        lastInstEnd = 0x0

        cur_bb_str = bb_func_map[bb.getMinAddress().getOffset()]

        while codeUnits.hasNext():
            codeUnit = codeUnits.next()

            if not isinstance(codeUnit, InstructionDB):
                continue

            lastInstStart = codeUnit.getAddress().getOffset()
            lastInstEnd = lastInstStart + codeUnit.getLength()
            successors = bb.getDestinations(monitor)

        idx = 0
        sucSet = set()
        while successors.hasNext():
            sucBBRef = successors.next()
            sucBBRefAddr = sucBBRef.getReferent().getOffset()
            # the reference is not in the last instruction
            if sucBBRefAddr < lastInstStart or sucBBRefAddr >= lastInstEnd:
                continue

            sucBB = sucBBRef.getDestinationBlock()
            sucOffset = sucBB.getFirstStartAddress().getOffset()
            if sucOffset in sucSet:
                continue

            if sucOffset not in bb_func_map:
                continue

            idx += 1

            currInsnAddr = sucBBRef.getReferent().getOffset()
            currBBAddr = bb.getMinAddress().getOffset()
            flowType = sucBBRef.getFlowType()

            edgeAttrs = 'color=cyan4 style=solid'

            edgeAttrs += ' tooltip="%s"' % str(flowType)
            G += (('  bb_%x -> %s [%s];\n') \
                    % (currBBAddr, bb_func_map[sucOffset], 
                       edgeAttrs))

            sucSet.add(sucOffset)

    return G

def dumpBlocks():
    bbModel = BasicBlockModel(currentProgram)
    functionManager = currentProgram.getFunctionManager()

    # record the basic block that has been added by functions
    bb_set = set()
    # get all functions
    funcs_set = set()
    for func in functionManager.getFunctions(True):
        # we skip external functions
        if func.isExternal():
            continue

        func_va = func.getEntryPoint().getOffset()
        if func_va in funcs_set:
            continue

        G = ('''digraph "func 0x%x" {
  newrank=true;
  // Flow Type Legend
''' % func_va)

        funcs_set.add(func_va)
        codeBlockIterator = bbModel.getCodeBlocksContaining(func.getBody(), monitor);


        # iter over the basic blocks
        bb_func_map = dict()
        bb_func_set = set()
        while codeBlockIterator.hasNext(): 
            bb = codeBlockIterator.next()
            bb_set.add(bb.getMinAddress().getOffset())
            bb_func_set.add(bb)
            G = addBB(bb, G, bb_func_map)

        G = addSuccessors(bb_func_set, bb_func_map, G)

        G += '}'

        with open('/home/svieg/projects/maitrise/MemSan/cfg/%s.dot' % func.getName(), 'w') as dot_output:
            dot_output.write(G)
    

if __name__ == "__main__":
    dumpBlocks()
